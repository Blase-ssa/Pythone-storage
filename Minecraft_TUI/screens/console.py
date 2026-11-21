from textual import work
from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import Input, Log


class ConsoleView(Vertical):
    def compose(self) -> ComposeResult:
        yield Log(id="console-log", highlight=True)
        yield Input(placeholder="RCON command, e.g. list  or  say hello", id="console-input")

    def on_mount(self) -> None:
        self.query_one("#console-log", Log).write_line(
            "Type a command and press Enter. This talks to rcon-cli."
        )

    def on_input_submitted(self, event: Input.Submitted) -> None:
        command = event.value.strip()
        if not command:
            return
        event.input.value = ""
        self.query_one("#console-log", Log).write_line(f"> {command}")
        self.send(command)

    @work(thread=True)
    def send(self, command: str) -> None:
        try:
            result = self.app.rcon.send_command(command)
            line = result if result else "(empty response)"
        except RuntimeError as exc:
            line = f"error: {exc}"
        self.app.call_from_thread(self._append, line)

    def _append(self, line: str) -> None:
        self.query_one("#console-log", Log).write_line(line)
