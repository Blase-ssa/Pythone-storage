from textual import work
from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import Button, Static

from screens.modals import ConfirmModal
from services import system as system_service


class SystemView(Vertical):
    def compose(self) -> ComposeResult:
        yield Static("Server control via RCON.")
        with Horizontal(id="system-actions"):
            yield Button("Save All", id="save", variant="primary")
            yield Button("Restart", id="restart", variant="error")
        yield Static("", id="system-result")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "save":
            self._run("save-all", lambda: system_service.save_all(self.app.rcon))
        elif event.button.id == "restart":

            def done(ok: bool) -> None:
                if ok:
                    self._run("restart", lambda: system_service.restart(self.app.rcon))

            self.app.push_screen(ConfirmModal("Restart the Minecraft server?"), done)

    @work(thread=True)
    def _run(self, label: str, fn) -> None:
        try:
            result = fn()
            text = result or f"{label} ok"
        except RuntimeError as exc:
            text = f"{label} failed: {exc}"
        self.app.call_from_thread(self._show, text)

    def _show(self, text: str) -> None:
        self.query_one("#system-result", Static).update(text)
