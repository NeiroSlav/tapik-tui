from uuid import UUID

from textual.app import ComposeResult
from textual.containers import Vertical

from widgets.active_chat.msg_input import MessageInputWidget
from widgets.active_chat.msg_list.msg_list import MessageListWidget


class ActiveChatWidget(Vertical):
    """Активный чат."""

    def __init__(self, chat_id: UUID):
        super().__init__()
        self.chat_id = chat_id

    def compose(self) -> ComposeResult:
        yield MessageListWidget(self.chat_id)
        yield MessageInputWidget(self.chat_id)
