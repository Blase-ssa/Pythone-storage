from textual import work
from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import Static

from services.dashboard import DashboardStatus, fetch_status


class DashboardView(Vertical):
    def compose(self) -> ComposeResult:
        yield Static("Connecting…", id="dash-body")

    def on_mount(self) -> None:
        self.refresh_status()
        self.set_interval(5.0, self.refresh_status)

    def refresh_status(self) -> None:
        self.load_status()

    @work(exclusive=True, thread=True)
    def load_status(self) -> None:
        status = fetch_status(self.app.rcon)
        self.app.call_from_thread(self._show_status, status)

    def _show_status(self, status: DashboardStatus) -> None:
        if status.connected:
            body = (
                f"RCON  {status.host}:{status.port}\n"
                f"Status  connected\n"
                f"Online  {status.online}\n\n"
                f"{status.list_raw}"
            )
        else:
            body = (
                f"RCON  {status.host}:{status.port}\n"
                f"Status  disconnected\n"
                f"Error   {status.error}"
            )
        self.query_one("#dash-body", Static).update(body)
