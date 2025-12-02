from uuid import UUID

from rich.align import Align
from rich.text import Text
from textual.widget import Widget

from store import RootStore


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

    def __init__(self, root_store: RootStore, chat_id: UUID):
        super().__init__()
        self.chat_id = chat_id
        self.root_store = root_store

    def render(self):
        chat = self.root_store.chats.get_chat(self.chat_id)
        text = Text(chat.name, style="bold")
        return Align.center(text)
