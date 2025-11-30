from textual.widget import Widget

from core.entities import Chat


class ChatWidget(Widget):
    """Один блок сообщения."""

    DEFAULT_CSS = """
    ChatWidget {
        width: 100%;
        height: 4;
        padding: 0 2;

        background: $surface 50%;
        border: tall $surface 0%;
    }

    ChatWidget.selected {
        background: $accent 20%;
        border: tall $accent;
    }
    """

    def __init__(self, chat: Chat, is_selected: bool):
        super().__init__()
        self.chat = chat
        self.is_selected = is_selected
        self.set_class(self.is_selected, "selected")

    def render(self):
        msg_time = self.chat.last_msg.time.strftime("%H:%M")
        first_line = f"[b]{self.chat.name:<20}[/b] • {msg_time}"

        msg_preview = f"{self.chat.last_msg.author}: {self.chat.last_msg.text}"
        second_line = msg_preview[0:50] if len(msg_preview) > 50 else msg_preview

        return f"{first_line}\n {second_line}"
