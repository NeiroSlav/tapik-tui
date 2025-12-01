from uuid import UUID

from rich.align import Align
from rich.text import Text
from textual.widget import Widget

from store.chat import chat_store


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
        chat = chat_store.get_chat(self.chat_id)
        text = Text(chat.name, style="bold")
        return Align.center(text)
