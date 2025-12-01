from textual.containers import Horizontal

from core.entities import Message
from ui.widgets.active_chat.msg_list.msg_bbl import MessageBubbleWidget
from utils.parsers import is_self_message


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
        is_self = is_self_message(message)
        self.set_class(is_self, "self")
        self.set_class(not is_self, "other")

    def compose(self):
        # сам bubble сообщения
        yield MessageBubbleWidget(self.message)
