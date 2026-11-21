from dataclasses import dataclass

from libs.rcon import RconClient
from libs.players import parse_list_output


@dataclass
class DashboardStatus:
    connected: bool
    host: str
    port: int
    online: int
    list_raw: str
    error: str = ""


def fetch_status(rcon: RconClient) -> DashboardStatus:
    try:
        raw = rcon.list_players()
        online = len(parse_list_output(raw))
        return DashboardStatus(
            connected=True,
            host=rcon.host,
            port=rcon.port,
            online=online,
            list_raw=raw,
        )
    except RuntimeError as exc:
        return DashboardStatus(
            connected=False,
            host=rcon.host,
            port=rcon.port,
            online=0,
            list_raw="",
            error=str(exc),
        )
