from __future__ import annotations

import argparse
import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping

DEFAULT_HOST = "papermc"
DEFAULT_PORT = 25575
DEFAULT_PASSWORD = "secret"
DEFAULT_ENV_FILE = ".env"
DEFAULT_CONFIG_FILE = "config.json"

_ENV_HOST = "MC_RCON_HOST"
_ENV_PORT = "MC_RCON_PORT"
_ENV_PASSWORD = "MC_RCON_PASS"


@dataclass(frozen=True)
class Settings:
    host: str
    port: int
    password: str


def load_settings(
    argv: list[str] | None = None,
    environ: Mapping[str, str] | None = None,
) -> Settings:
    """CLI > config.json > environment > .env > defaults."""
    args = _parse_args(argv)
    env = environ if environ is not None else os.environ

    env_file = Path(args.env_file) if args.env_file else Path(DEFAULT_ENV_FILE)
    config_file = Path(args.config) if args.config else Path(DEFAULT_CONFIG_FILE)

    values: dict[str, Any] = {
        "host": DEFAULT_HOST,
        "port": DEFAULT_PORT,
        "password": DEFAULT_PASSWORD,
    }
    _merge(values, _from_dotenv(env_file, required=bool(args.env_file)))
    _merge(values, _from_environ(env))
    _merge(values, _from_json(config_file, required=bool(args.config)))
    _merge(
        values,
        {
            "host": args.host,
            "port": args.port,
            "password": args.password,
        },
    )
    return Settings(
        host=str(values["host"]),
        port=_as_port(values["port"]),
        password=str(values["password"]),
    )


def _parse_args(argv: list[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Minecraft RCON TUI")
    parser.add_argument("--host", help="Server hostname or IP")
    parser.add_argument("--port", type=int, help="RCON port")
    parser.add_argument("--password", help="RCON password")
    parser.add_argument(
        "--config",
        help=f"Path to config.json (default: {DEFAULT_CONFIG_FILE} if it exists)",
    )
    parser.add_argument(
        "--env-file",
        help=f"Path to .env (default: {DEFAULT_ENV_FILE} if it exists)",
    )
    return parser.parse_args(argv)


def _merge(target: dict[str, Any], overlay: Mapping[str, Any]) -> None:
    for key, value in overlay.items():
        if value is not None and value != "":
            target[key] = value


def _from_environ(env: Mapping[str, str]) -> dict[str, Any]:
    return {
        "host": env.get(_ENV_HOST) or None,
        "port": env.get(_ENV_PORT) or None,
        "password": env.get(_ENV_PASSWORD) or None,
    }


def _from_json(path: Path, required: bool) -> dict[str, Any]:
    if not path.is_file():
        if required:
            raise FileNotFoundError(f"config file not found: {path}")
        return {}

    with path.open(encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"{path} must contain a JSON object")

    return {
        "host": data.get("host"),
        "port": data.get("port"),
        "password": data.get("password"),
    }


def _from_dotenv(path: Path, required: bool) -> dict[str, Any]:
    if not path.is_file():
        if required:
            raise FileNotFoundError(f".env file not found: {path}")
        return {}

    raw: dict[str, str] = {}
    for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if stripped.startswith("export "):
            stripped = stripped[len("export ") :].strip()
        if "=" not in stripped:
            raise ValueError(f"{path}:{line_no}: expected KEY=VALUE")
        key, _, value = stripped.partition("=")
        raw[key.strip()] = _unquote(value.strip())

    return {
        "host": raw.get(_ENV_HOST) or None,
        "port": raw.get(_ENV_PORT) or None,
        "password": raw.get(_ENV_PASSWORD) if raw.get(_ENV_PASSWORD) is not None else None,
    }


def _unquote(value: str) -> str:
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
        return value[1:-1]
    return value


def _as_port(value: Any) -> int:
    try:
        port = int(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"invalid RCON port: {value!r}") from exc
    if not 1 <= port <= 65535:
        raise ValueError(f"invalid RCON port: {port}")
    return port
