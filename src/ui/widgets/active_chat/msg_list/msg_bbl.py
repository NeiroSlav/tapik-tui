from textual.widget import Widget

from ui.viewmodels.message_vm import MessageVM


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

    def __init__(self, message_vm: MessageVM):
        super().__init__()
        self.message_vm = message_vm

        is_self = self.message_vm.is_self
        self.set_class(is_self, "self")
        self.set_class(not is_self, "other")

    def render(self):
        return (
            f"[b]{self.message_vm.sender_name}[/b] • {self.message_vm.str_time}\n"
            f"{self.message_vm.full_text}"
        )
