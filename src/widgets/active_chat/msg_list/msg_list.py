import asyncio

from textual.containers import VerticalScroll
from textual.reactive import reactive

from core.entities import Message
from store.message import message_store
from utils.logger import logger
from widgets.active_chat.msg_list.msg_row import MessageRowWidget


class MessageListWidget(VerticalScroll):
    """Список сообщений."""

    DEFAULT_CSS = """
    MessageListWidget {
        width: 100%;
        height: 100%;
        padding: 0 0;
    }

    MessageListWidget > ScrollBar {
        background: grey;
        width: 1;
    }

    MessageListWidget > ScrollBar > Thumb {
        background: white;
    }

    """

    messages = reactive([])  # список объектов сообщений

    def __init__(self):
        super().__init__()
        message_store.subscribe(self._subscibe_cb)
        self.messages = message_store.messages

    async def on_mount(self):
        await self.render_messages()

    async def render_messages(self):
        """Полностью перерисовать список."""
        self.remove_children()
        for msg in self.messages:
            widget = MessageRowWidget(msg)
            await self.mount(widget)
        self.scroll_end(animate=False)

    def _subscibe_cb(self, new_messages: list[Message]):
        logger("Коллбек отработал")
        self.messages = new_messages
        asyncio.create_task(self.render_messages())
