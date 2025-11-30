from datetime import datetime
from uuid import UUID

from textual.app import ComposeResult
from textual.containers import Horizontal
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import Input

from core.entities import Message
from store.chat import chat_store
from store.message import message_store


class MessageInputWidget(Widget):
    text = reactive("")

    DEFAULT_CSS = """
    MessageInputWidget {
        dock: bottom;
        width: 100%;
        height: 3;
        padding: 0 1 0 0;
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

    async def on_input_changed(self, event: Input.Changed) -> None:
        self.text = event.value

    async def on_input_submitted(self, event: Input.Submitted):
        text = self.input.value.strip()
        if text:
            await self._post_msg(text)
            self.input.value = ""

    async def _post_msg(self, text: str) -> None:
        if text.startswith("-"):
            self._post_old_msg(text)
        else:
            self._post_new_msg(text)

    def _post_new_msg(self, text: str) -> None:
        message = Message(
            text=text,
            author="Me",
            time=datetime.now(),
            is_self=True,
            local_id=message_store.test_get_last_id(self.chat_id) + 1,
            chat_id=self.chat_id,
        )
        message_store.add_messages([message])
        chat_store.upd_last_msg(self.chat_id, message)

    def _post_old_msg(self, text: str) -> None:
        message_store.add_messages(
            [
                Message(
                    text=text,
                    author="Me",
                    time=datetime.now(),
                    is_self=True,
                    local_id=message_store.test_get_first_id(self.chat_id) - 1,
                    chat_id=self.chat_id,
                )
            ]
        )
