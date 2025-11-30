from textual.containers import VerticalScroll
from textual.reactive import reactive
from textual.widget import Widget

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

        # Подписка на обновление сообщений
        message_store.subscribe(callback=self._subscibe_cb)
        self.messages = message_store.messages

        # Мапы списка сообщений к сообщениям
        self._message_widgets: dict[int, Widget] = {}
        self.oldest_msg_id = self.messages[0].local_id
        self.newest_msg_id = self.messages[-1].local_id

    async def _subscibe_cb(self, new_messages: list[Message]):
        logger("Коллбек отработал")
        self.messages = new_messages
        await self._render_diff_messages()

    # Отрисовки при изменениях

    async def _render_diff_messages(self):
        """Вычисление разницы сообщений, и отрисовка неотрисованных"""
        newer_msgs = [m for m in self.messages if m.local_id > self.newest_msg_id]
        older_msgs = [m for m in self.messages if m.local_id < self.oldest_msg_id]

        if newer_msgs:
            await self._render_newer_diffs(newer_msgs)
            self.newest_msg_id = max([m.local_id for m in newer_msgs])
            self.scroll_end(animate=False)

        if older_msgs:
            await self._render_older_diffs(older_msgs)
            self.oldest_msg_id = min([m.local_id for m in older_msgs])

    async def _render_newer_diffs(self, msgs: list[Message]):
        """Отрисовка новых сообщений"""
        for msg in msgs:
            widget = MessageRowWidget(msg)
            self._message_widgets[msg.local_id] = widget
            await self.mount(widget)

    async def _render_older_diffs(self, msgs: list[Message]):
        """Отрисовка старых сообщений"""
        oldest_widget = self._message_widgets[self.oldest_msg_id]
        for msg in msgs:
            widget = MessageRowWidget(msg)
            self._message_widgets[msg.local_id] = widget
            await self.mount(widget, before=oldest_widget)
            oldest_widget = widget

    # Отрисовки при монтировании

    async def on_mount(self):
        """Действия при монтировании"""
        await self._render_all_messages()

    async def _render_all_messages(self):
        """Полностью перерисовать список."""
        self.remove_children()
        for msg in self.messages:
            widget = MessageRowWidget(msg)
            self._message_widgets[msg.local_id] = widget
            await self.mount(widget)
        self.scroll_end(animate=False)
