import re
from dataclasses import dataclass
from typing import List

from libs.players import get_online_players
from libs.rcon import RconClient

_GAMEMODE = {
    0: "Survival",
    1: "Creative",
    2: "Adventure",
    3: "Spectator",
}
_GAMEMODE_VALUE = re.compile(r"(-?\d+)\s*$")


@dataclass
class PlayerInfo:
    name: str
    ping: str = "—"
    gamemode: str = "—"
    status: str = "Online"


def _gamemode_for(rcon: RconClient, name: str) -> str:
    try:
        output = rcon.send_command(f"data get entity {name} playerGameType")
    except RuntimeError:
        return "—"

    match = _GAMEMODE_VALUE.search(output)
    if not match:
        return "—"
    try:
        return _GAMEMODE.get(int(match.group(1)), "—")
    except ValueError:
        return "—"


def fetch_online_players(rcon: RconClient) -> List[PlayerInfo]:
    names = get_online_players(rcon)
    return [
        PlayerInfo(name=name, gamemode=_gamemode_for(rcon, name))
        for name in names
    ]
