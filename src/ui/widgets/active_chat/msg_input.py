from uuid import UUID

from textual.app import ComposeResult
from textual.containers import Horizontal
from textual.widget import Widget
from textual.widgets import Input

from ui.root_mixin import RootProviderMixin


class MessageInputWidget(Widget, RootProviderMixin):

    DEFAULT_CSS = """
    MessageInputWidget {
        dock: bottom;
        height: 3;
    }

    #msg-input {
        width: 100%;
        height: 3;
        background: $surface 50%;
        border: tall $surface 0%;
    }
    """

    def __init__(self, chat_id: UUID):
        super().__init__()
        self.chat_id = chat_id

    def compose(self) -> ComposeResult:
        with Horizontal():
            self.input = Input(placeholder="Введите сообщение...", id="msg-input")
            yield self.input

    async def on_input_submitted(self, event: Input.Submitted):
        text = self.input.value.strip()
        if text:
            self.root_actions.send_message(self.chat_id, text)
            self.input.value = ""
