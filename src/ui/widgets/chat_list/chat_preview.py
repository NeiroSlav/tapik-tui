from typing import Callable
from uuid import UUID

from textual.events import Click
from textual.widget import Widget

from ui.viewmodels.chat_vm import ChatVM


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
        chat_vm: ChatVM,
        is_active: bool,
        is_cursor: bool,
        on_chat_click: Callable[[UUID], None],
    ):
        super().__init__()
        self.chat_vm = chat_vm
        self.is_active = is_active
        self.is_cursor = is_cursor
        self.on_click_cb = on_chat_click
        self.set_class(self.is_active, "active")
        self.set_class(self.is_cursor and not self.is_active, "cursor")

    def render(self):
        msg_time = self.chat_vm.message_vm.str_time
        first_line = f"[b]{self.chat_vm.name:<20}[/b] • {msg_time}"

        sender_name = self.chat_vm.message_vm.sender_name
        msg_preview = f"{sender_name}: {self.chat_vm.message_vm.str_content}"
        second_line = msg_preview[0:50] if len(msg_preview) > 50 else msg_preview

        return f"{first_line}\n {second_line}"

    def on_click(self, event: Click) -> None:
        self.on_click_cb(self.get_chat_id())

    def get_chat_id(self) -> UUID:
        return self.chat_vm.chat.chat_id
