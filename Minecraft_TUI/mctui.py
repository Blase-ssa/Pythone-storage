#!/usr/bin/python3

import os

from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.widgets import Footer, TabbedContent, TabPane

from libs.rcon import RconClient
from screens import (
    ConsoleView,
    DashboardView,
    PlayersView,
    PluginsView,
    SystemView,
    WorldView,
)


def _rcon_from_env() -> RconClient:
    return RconClient(
        host=os.environ.get("MCTUI_HOST", "papermc"),
        port=int(os.environ.get("MCTUI_PORT", "25575")),
        password=os.environ.get("MCTUI_PASSWORD", "secret"),
        binary=os.environ.get("MCTUI_RCON_BIN", "rcon-cli"),
    )


class McTui(App):
    CSS_PATH = "mctui.tcss"
    TITLE = "Minecraft RCON"
    BINDINGS = [
        Binding("1", "show_tab('dashboard')", "Dashboard", show=False),
        Binding("2", "show_tab('players')", "Players", show=False),
        Binding("3", "show_tab('world')", "World", show=False),
        Binding("4", "show_tab('plugins')", "Plugins", show=False),
        Binding("5", "show_tab('console')", "Console", show=False),
        Binding("6", "show_tab('system')", "System", show=False),
        Binding("q", "quit", "Quit"),
    ]

    def __init__(self) -> None:
        super().__init__()
        self.rcon = _rcon_from_env()

    def compose(self) -> ComposeResult:
        with TabbedContent(initial="dashboard"):
            with TabPane("Dashboard", id="dashboard"):
                yield DashboardView()
            with TabPane("Players", id="players"):
                yield PlayersView()
            with TabPane("World", id="world"):
                yield WorldView()
            with TabPane("Plugins", id="plugins"):
                yield PluginsView()
            with TabPane("Console", id="console"):
                yield ConsoleView()
            with TabPane("System", id="system"):
                yield SystemView()
        yield Footer()

    def action_show_tab(self, tab_id: str) -> None:
        tabs = self.query_one(TabbedContent)
        tabs.active = tab_id

    def on_tabbed_content_tab_activated(self, event: TabbedContent.TabActivated) -> None:
        if event.pane.id == "players":
            self.query_one("#players-table").focus()
        elif event.pane.id == "console":
            self.query_one("#console-input").focus()


if __name__ == "__main__":
    McTui().run()
