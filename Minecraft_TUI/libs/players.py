import re
from typing import List

from libs.rcon import RconClient

_LIST_NAMES = re.compile(r":\s*(.*)$")
_UUID_SUFFIX = re.compile(r"\s*\([^)]*\)\s*$")


def parse_list_output(output: str) -> List[str]:
    match = _LIST_NAMES.search(output)
    if not match:
        return []

    players = match.group(1).strip()
    if not players:
        return []

    names = []
    for raw in players.split(","):
        name = _UUID_SUFFIX.sub("", raw).strip()
        if name:
            names.append(name)
    return names


def get_online_players(rcon: RconClient) -> List[str]:
    return parse_list_output(rcon.send_command("list"))
