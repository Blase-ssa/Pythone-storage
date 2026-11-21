from libs.rcon import RconClient


def save_all(rcon: RconClient) -> str:
    return rcon.save_all()


def restart(rcon: RconClient) -> str:
    return rcon.restart()
