from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import Static


class PluginsView(Vertical):
    def compose(self) -> ComposeResult:
        yield Static("Plugins — not in MVP yet.\nPlugin list via RCON is server-specific.")
