import subprocess


class RconClient:
    def __init__(
        self,
        host: str,
        port: int,
        password: str,
        binary: str = "rcon-cli",
        timeout: float = 10.0,
    ):
        self.host = host
        self.port = port
        self.password = password
        self.binary = binary
        self.timeout = timeout

    def send_command(self, command: str) -> str:
        try:
            result = subprocess.run(
                [
                    self.binary,
                    "--host",
                    self.host,
                    "--port",
                    str(self.port),
                    "--password",
                    self.password,
                    command,
                ],
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=self.timeout,
            )
        except FileNotFoundError as exc:
            raise RuntimeError(
                f"{self.binary} not found. Install rcon-cli and put it on PATH."
            ) from exc
        except subprocess.TimeoutExpired as exc:
            raise RuntimeError(f"rcon-cli timed out after {self.timeout}s") from exc

        if result.returncode != 0:
            err = (result.stderr or result.stdout or "rcon-cli failed").strip()
            raise RuntimeError(err)

        return (result.stdout or "").strip()

    def list_players(self) -> str:
        return self.send_command("list")

    def whitelist_add(self, player: str) -> str:
        return self.send_command(f"whitelist add {player}")

    def whitelist_remove(self, player: str) -> str:
        return self.send_command(f"whitelist remove {player}")

    def kick(self, player: str, reason: str = "") -> str:
        cmd = f"kick {player}"
        if reason:
            cmd += f" {reason}"
        return self.send_command(cmd)

    def ban(self, player: str, reason: str = "") -> str:
        cmd = f"ban {player}"
        if reason:
            cmd += f" {reason}"
        return self.send_command(cmd)

    def op(self, player: str) -> str:
        return self.send_command(f"op {player}")

    def deop(self, player: str) -> str:
        return self.send_command(f"deop {player}")

    def teleport(self, player: str, destination: str) -> str:
        return self.send_command(f"tp {player} {destination}")

    def say(self, message: str) -> str:
        return self.send_command(f"say {message}")

    def save_all(self) -> str:
        return self.send_command("save-all")

    def restart(self) -> str:
        return self.send_command("restart")
