# Dev status

Last updated: 2026-11-21

The project is an **MVP**: a Textual shell over `rcon-cli` with a working Players tab and a few other live screens. It is not a full server panel.

## Works

- App shell with tabs: Dashboard, Players, World, Plugins, Console, System
- Settings from CLI, `config.json`, environment, and `.env` (`CLI > json > env > .env > defaults`)
- Env / `.env` names: `MC_RCON_HOST`, `MC_RCON_PORT`, `MC_RCON_PASS`
- RCON via `rcon-cli` subprocess (timeout, missing-binary error)
- **Dashboard**: host, port, connected/disconnected, online count, raw `list` output; refresh every 5s
- **Players**: online names from `list`; GameMode via `data get entity <name> playerGameType`; Kick / Ban / Op / Teleport; auto-refresh every 8s
- **Console**: send an arbitrary RCON command and show the reply
- **System**: `save-all`; `restart` with a confirm dialog
- RCON calls run on worker threads so the UI does not freeze on a slow `rcon-cli`

## Does not work / not built

- **World** tab: placeholder only (no time, weather, difficulty)
- **Plugins** tab: placeholder only (no plugin list)
- **Ping** column: always `—` (vanilla RCON has no player ping)
- **Status** column: always `Online` for names returned by `list` (no offline / vanished / vanished-from-tab list)
- **Deop**, whitelist, `say`, and other `RconClient` helpers: exist on the client, not wired in the UI
- Native RCON socket: not implemented; `rcon-cli` must be installed
- Packaging, installer, tests in the repo, logging, multi-server profiles

## Known limits

- GameMode depends on `data get entity … playerGameType`. If the server rejects that NBT path, the cell stays `—`.
- One extra RCON call per online player for GameMode; a busy tab can feel slow.
- Defaults (`papermc` / `secret`) match a local Docker-style setup and will fail against a real server until configured.
- Password on the command line is visible in the process list.
- Headless / CI UI coverage is not in the repository; only ad-hoc checks were run during development.

## Next (not scheduled)

Useful follow-ups if the MVP stays: World (time/weather), a plugin list that does not assume a specific core, player ping from a Paper/plugin command if available, deop/whitelist in Players, automated tests for `libs/config.py` and `list` parsing.
