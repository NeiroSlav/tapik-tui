from typing import Callable
from uuid import UUID

from textual.events import Click
from textual.widget import Widget

from core.entities import Chat
from utils.parsers import get_sender_name


class ChatPreviewWidget(Widget):
    """Один блок сообщения."""

    DEFAULT_CSS = """
    ChatPreviewWidget {
        width: 100%;
        height: 4;
        padding: 0 2;

        background: $surface 50%;
        border: tall $surface 0%;
    }

    ChatPreviewWidget.active {
        background: $accent 20%;
        border: tall $accent;
    }

    ChatPreviewWidget.cursor {
        background: $surface 100%;
        border: tall $surface 0%;
    }

    """

    def __init__(
        self,
        chat: Chat,
        is_active: bool,
        is_cursor: bool,
        on_chat_click: Callable[[UUID], None],
    ):
        super().__init__()
        self.chat = chat
        self.is_active = is_active
        self.is_cursor = is_cursor
        self.on_click_cb = on_chat_click
        self.set_class(self.is_active, "active")
        self.set_class(self.is_cursor and not self.is_active, "cursor")

    def render(self):
        msg_time = self.chat.last_msg.time.strftime("%H:%M")
        first_line = f"[b]{self.chat.name:<20}[/b] • {msg_time}"

        sender_name = get_sender_name(self.chat.last_msg)
        msg_preview = f"{sender_name}: {self.chat.last_msg.text}"
        second_line = msg_preview[0:50] if len(msg_preview) > 50 else msg_preview

        return f"{first_line}\n {second_line}"

    def on_click(self, event: Click) -> None:
        self.on_click_cb(self.chat.chat_id)
