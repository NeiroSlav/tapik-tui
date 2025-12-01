from textual.containers import Horizontal

from core.entities import Message
from widgets.active_chat.msg_list.msg_bbl import MessageBubbleWidget


class MessageRowWidget(Horizontal):
    """Обёртка сообщения для выравнивания по горизонтали"""

    DEFAULT_CSS = """
    MessageRowWidget {
        width: 100%;
        height: auto;
    }
    MessageRowWidget.self {
        align-horizontal: right;
    }
    MessageRowWidget.other {
        align-horizontal: left;
    }
    """

    def __init__(self, message: Message):
        super().__init__()
        self.message = message

        # класс для выравнивания
        self.set_class(message.is_self, "self")
        self.set_class(not message.is_self, "other")

    def compose(self):
        # сам bubble сообщения
        yield MessageBubbleWidget(self.message)
