from textual.app import ComposeResult
from textual.containers import Vertical

from widgets.active_chat.msg_input import MessageInputWidget
from widgets.active_chat.msg_list.msg_list import MessageListWidget


class ActiveChatWidget(Vertical):
    """Активный чат."""

    def compose(self) -> ComposeResult:
        yield MessageListWidget()
        yield MessageInputWidget()
