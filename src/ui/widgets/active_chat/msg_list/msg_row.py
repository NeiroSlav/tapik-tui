from textual.containers import Horizontal

from ui.viewmodels.message_vm import MessageVM
from ui.widgets.active_chat.msg_list.msg_bbl import MessageBubbleWidget


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

    def __init__(self, message_vm: MessageVM):
        super().__init__()
        self.message_vm = message_vm

        # класс для выравнивания
        is_self = self.message_vm.is_self
        self.set_class(is_self, "self")
        self.set_class(not is_self, "other")

    def compose(self):
        # сам bubble сообщения
        yield MessageBubbleWidget(self.message_vm)
