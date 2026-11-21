from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import Static


class WorldView(Vertical):
    def compose(self) -> ComposeResult:
        yield Static("World — not in MVP yet.\nTime, weather, difficulty will go here.")
