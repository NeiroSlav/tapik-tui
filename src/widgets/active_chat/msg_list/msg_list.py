from textual.containers import VerticalScroll
from textual.reactive import reactive

from core.entities import Message
from widgets.active_chat.msg_list.msg_row import MessageRowWidget


class MessageListWidget(VerticalScroll):
    """Список сообщений."""

    DEFAULT_CSS = """
    MessageListWidget {
        width: 100%;
        height: 100%;
        padding: 0 0;
    }
    """

    messages = reactive([])  # список объектов сообщений

    def __init__(self, messages: list[Message] | None = None):
        super().__init__()
        self.messages = messages or []

    async def on_mount(self):
        await self.render_messages()

    async def render_messages(self):
        """Полностью перерисовать список."""
        self.remove_children()

        for msg in self.messages:
            widget = MessageRowWidget(msg)
            await self.mount(widget)

        self.scroll_end(animate=False)

    async def add_message(self, msg: Message):
        """Добавить одно сообщение и отрендерить его."""
        self.messages = self.messages + [msg]  # триггерит reactive
