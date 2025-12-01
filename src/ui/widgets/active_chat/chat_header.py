from uuid import UUID

from rich.align import Align
from rich.text import Text
from textual.widget import Widget

from store.app_state import app_state


class ChatHeaderWidget(Widget):
    """Шапка активного чата"""

    DEFAULT_CSS = """
    ChatHeaderWidget {
        width: 100%;
        height: 3;
        padding: 0 2;

        background: $surface 50%;
        border: tall $surface 0%;
    }
    """

    def __init__(self, chat_id: UUID):
        super().__init__()
        self.chat_id = chat_id

    def render(self):
        chat = app_state.chats.get_chat(self.chat_id)
        text = Text(chat.name, style="bold")
        return Align.center(text)
