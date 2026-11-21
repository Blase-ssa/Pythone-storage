# Minecraft RCON TUI

Terminal UI for a Minecraft server over RCON. The app talks to the server through [`rcon-cli`](https://github.com/itzg/rcon-cli), not a native RCON library.

```
┌ Dashboard | Players | World | Plugins | Console | System ──┐
│                                                             │
│                      Content Area                           │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Requirements

- Python 3.10+
- [`rcon-cli`](https://github.com/itzg/rcon-cli) on `PATH`
- A Minecraft server with RCON enabled (`enable-rcon=true` in `server.properties`)

## Install

```powershell
pip install -r requirements.txt
```

## Run

```powershell
python mctui.py
```

Keys **1–6** switch tabs. **Q** quits.

| Key | Tab |
| --- | --- |
| 1 | Dashboard |
| 2 | Players |
| 3 | World |
| 4 | Plugins |
| 5 | Console |
| 6 | System |

On **Players**:

| Key | Action |
| --- | --- |
| K | Kick (optional reason) |
| B | Ban (optional reason) |
| O | Op |
| T | Teleport (player name or `x y z`) |
| R | Refresh list |

## Configuration

Only three values are needed: RCON host, port, and password.

Sources, strongest first:

1. Command line
2. `config.json`
3. Environment variables
4. `.env`
5. Built-in defaults (`papermc`, `25575`, `secret`)

Each field is merged on its own. `--host` does not wipe port or password from a lower source.

### Command line

```powershell
python mctui.py --host 127.0.0.1 --port 25575 --password secret
```

Optional paths:

```powershell
python mctui.py --config D:\path\config.json --env-file D:\path\.env
```

If `--config` or `--env-file` is given and the file is missing, the app exits with an error. If they are omitted, `config.json` and `.env` in the current directory are used when present.

### `config.json`

```json
{
  "host": "127.0.0.1",
  "port": 25575,
  "password": "secret"
}
```

### Environment and `.env`

```
MC_RCON_HOST=127.0.0.1
MC_RCON_PORT=25575
MC_RCON_PASS=secret
```

`.env` is read as a file. It is not loaded into `os.environ`, so real environment variables override it.

## Layout

| Path | Role |
| --- | --- |
| `mctui.py` | App entry |
| `libs/config.py` | Settings merge |
| `libs/rcon.py` | `rcon-cli` wrapper |
| `services/` | RCON data (list, status, save/restart) |
| `screens/` | Textual tabs |

Current feature status is in [DEVSTATUS.md](DEVSTATUS.md).
