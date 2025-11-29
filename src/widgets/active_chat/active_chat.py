from textual.app import ComposeResult
from textual.containers import Vertical
from textual.reactive import reactive

from core.entities import Message
from widgets.active_chat.msg_input import MessageInputWidget
from widgets.active_chat.msg_list import MessageListWidget


class ActiveChatWidget(Vertical):
    """Активный чат."""

    messages = reactive([])  # список объектов сообщений

    def __init__(self, messages: list[Message]):
        super().__init__()
        self.messages = messages

    def compose(self) -> ComposeResult:
        yield MessageListWidget(self.messages)
        yield MessageInputWidget()
