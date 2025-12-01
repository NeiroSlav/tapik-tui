from textual.reactive import reactive
from textual.widget import Widget

from core.entities import Message


class MessageBubbleWidget(Widget):
    """Один блок сообщения."""

    DEFAULT_CSS = """
    MessageBubbleWidget {
        max-width: 80%;
        width: auto;
        height: auto;
        padding: 0 2;
    }

    MessageBubbleWidget.self {
        background: $accent 20%;
        border: tall $accent;
    }

    MessageBubbleWidget.other {
        background: $surface 50%;
        border: tall $surface 0%;
    }
    """

    text = reactive("")
    author = reactive("")
    timestamp = reactive("")
    is_self = reactive(False)

    def __init__(self, message: Message):
        super().__init__()
        self.text = message.text
        self.author = message.author
        self.timestamp = message.time.strftime("%H:%M")
        self.is_self = message.is_self

        self.set_class(self.is_self, "self")
        self.set_class(not self.is_self, "other")

    def render(self):
        # Можно рисовать красивее, с разметкой
        return f"[b]{self.author}[/b] • {self.timestamp}\n{self.text}"
