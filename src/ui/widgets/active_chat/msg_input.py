from datetime import datetime
from uuid import UUID

from textual.app import ComposeResult
from textual.containers import Horizontal
from textual.widget import Widget
from textual.widgets import Input

from core.entities import Message
from store import RootStore


class MessageInputWidget(Widget):

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

    def __init__(self, root_store: RootStore, chat_id: UUID):
        super().__init__()
        self.root_store = root_store
        self.chat_id = chat_id

    def compose(self) -> ComposeResult:
        with Horizontal():
            self.input = Input(placeholder="Введите сообщение...", id="msg-input")
            yield self.input

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
            user_id=self.root_store.current_user_id.get(),
            time=datetime.now(),
            local_id=self.root_store.messages.test_get_last_id(self.chat_id) + 1,
            chat_id=self.chat_id,
        )
        self.root_store.messages.add_messages([message])
        self.root_store.chats.upd_last_msg(self.chat_id, message)

    def _post_old_msg(self, text: str) -> None:
        self.root_store.messages.add_messages(
            [
                Message(
                    text=text,
                    user_id=self.root_store.current_user_id.get(),
                    time=datetime.now(),
                    local_id=self.root_store.messages.test_get_first_id(self.chat_id)
                    - 1,
                    chat_id=self.chat_id,
                )
            ]
        )
