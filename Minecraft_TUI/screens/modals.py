from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.screen import ModalScreen
from textual.widgets import Button, Input, Label, Static


class ReasonModal(ModalScreen[str | None]):
    def __init__(self, title: str, player: str) -> None:
        super().__init__()
        self._title = title
        self._player = player

    def compose(self) -> ComposeResult:
        with Vertical(id="modal"):
            yield Label(f"{self._title} {self._player}")
            yield Input(placeholder="reason (optional)", id="reason")
            with Horizontal(id="modal-buttons"):
                yield Button("Confirm", variant="error", id="ok")
                yield Button("Cancel", id="cancel")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "ok":
            self.dismiss(self.query_one("#reason", Input).value.strip())
        else:
            self.dismiss(None)

    def on_input_submitted(self, event: Input.Submitted) -> None:
        self.dismiss(event.value.strip())


class TeleportModal(ModalScreen[str | None]):
    def __init__(self, player: str) -> None:
        super().__init__()
        self._player = player

    def compose(self) -> ComposeResult:
        with Vertical(id="modal"):
            yield Label(f"Teleport {self._player}")
            yield Static("Target player or coordinates, e.g. Alex  or  0 64 0")
            yield Input(placeholder="destination", id="dest")
            with Horizontal(id="modal-buttons"):
                yield Button("Teleport", variant="primary", id="ok")
                yield Button("Cancel", id="cancel")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "ok":
            dest = self.query_one("#dest", Input).value.strip()
            self.dismiss(dest or None)
        else:
            self.dismiss(None)

    def on_input_submitted(self, event: Input.Submitted) -> None:
        dest = event.value.strip()
        self.dismiss(dest or None)


class ConfirmModal(ModalScreen[bool]):
    def __init__(self, message: str) -> None:
        super().__init__()
        self._message = message

    def compose(self) -> ComposeResult:
        with Vertical(id="modal"):
            yield Label(self._message)
            with Horizontal(id="modal-buttons"):
                yield Button("Confirm", variant="error", id="ok")
                yield Button("Cancel", id="cancel")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        self.dismiss(event.button.id == "ok")
