from textual import work
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, Vertical
from textual.widgets import Button, DataTable, Static

from screens.modals import ReasonModal, TeleportModal
from services.players import PlayerInfo, fetch_online_players


class PlayersView(Vertical):
    BINDINGS = [
        Binding("k", "kick", "Kick"),
        Binding("b", "ban", "Ban"),
        Binding("o", "op", "Op"),
        Binding("t", "teleport", "Teleport"),
        Binding("r", "refresh", "Refresh"),
    ]

    def compose(self) -> ComposeResult:
        table = DataTable(id="players-table", cursor_type="row", zebra_stripes=True)
        table.add_columns("Name", "Ping", "GameMode", "Status")
        yield table
        with Horizontal(id="player-actions"):
            yield Button("[K] Kick", id="kick", variant="warning")
            yield Button("[B] Ban", id="ban", variant="error")
            yield Button("[O] Op", id="op", variant="success")
            yield Button("[T] Teleport", id="teleport")
        yield Static("Select a player, then Kick / Ban / Op / Teleport.", id="players-hint")

    def on_mount(self) -> None:
        self.query_one(DataTable).focus()
        self.action_refresh()
        self.set_interval(8.0, self.action_refresh)

    def action_refresh(self) -> None:
        self.load_players()

    @work(exclusive=True, thread=True)
    def load_players(self) -> None:
        try:
            players = fetch_online_players(self.app.rcon)
            error = ""
        except RuntimeError as exc:
            players = []
            error = str(exc)
        self.app.call_from_thread(self._fill_table, players, error)

    def _fill_table(self, players: list[PlayerInfo], error: str) -> None:
        table = self.query_one("#players-table", DataTable)
        table.clear()
        for player in players:
            table.add_row(
                player.name,
                player.ping,
                player.gamemode,
                player.status,
                key=player.name,
            )
        hint = self.query_one("#players-hint", Static)
        if error:
            hint.update(f"RCON error: {error}")
        elif not players:
            hint.update("No players online.")
        else:
            hint.update(f"{len(players)} online. Select a row, then K / B / O / T.")

    def selected_player(self) -> str | None:
        table = self.query_one("#players-table", DataTable)
        if table.row_count == 0:
            return None
        row = table.get_row_at(table.cursor_row)
        return str(row[0]) if row else None

    def on_button_pressed(self, event: Button.Pressed) -> None:
        actions = {
            "kick": self.action_kick,
            "ban": self.action_ban,
            "op": self.action_op,
            "teleport": self.action_teleport,
        }
        action = actions.get(event.button.id or "")
        if action:
            action()

    def action_kick(self) -> None:
        player = self.selected_player()
        if not player:
            self.app.notify("Select a player first.", severity="warning")
            return

        def done(reason: str | None) -> None:
            if reason is None:
                return
            self._run_command(lambda: self.app.rcon.kick(player, reason), f"Kicked {player}")

        self.app.push_screen(ReasonModal("Kick", player), done)

    def action_ban(self) -> None:
        player = self.selected_player()
        if not player:
            self.app.notify("Select a player first.", severity="warning")
            return

        def done(reason: str | None) -> None:
            if reason is None:
                return
            self._run_command(lambda: self.app.rcon.ban(player, reason), f"Banned {player}")

        self.app.push_screen(ReasonModal("Ban", player), done)

    def action_op(self) -> None:
        player = self.selected_player()
        if not player:
            self.app.notify("Select a player first.", severity="warning")
            return
        self._run_command(lambda: self.app.rcon.op(player), f"Opped {player}")

    def action_teleport(self) -> None:
        player = self.selected_player()
        if not player:
            self.app.notify("Select a player first.", severity="warning")
            return

        def done(destination: str | None) -> None:
            if not destination:
                return
            self._run_command(
                lambda: self.app.rcon.teleport(player, destination),
                f"Teleported {player}",
            )

        self.app.push_screen(TeleportModal(player), done)

    @work(thread=True)
    def _run_command(self, fn, ok_message: str) -> None:
        try:
            result = fn()
            message = result or ok_message
            severity = "information"
        except RuntimeError as exc:
            message = str(exc)
            severity = "error"
        self.app.call_from_thread(self._after_command, message, severity)

    def _after_command(self, message: str, severity: str) -> None:
        self.app.notify(message, severity=severity)
        self.load_players()
