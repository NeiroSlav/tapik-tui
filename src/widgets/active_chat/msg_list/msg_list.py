from uuid import UUID

from textual.containers import VerticalScroll
from textual.reactive import reactive
from textual.widget import Widget

from core.entities import Message
from store.app_state import app_state
from widgets.active_chat.msg_list.msg_row import MessageRowWidget


class MessageListWidget(VerticalScroll):
    """Список сообщений."""

    DEFAULT_CSS = """
    MessageListWidget {
        width: 100%;
        height: 100%;
        padding: 0 0;
        margin: 0 0 3 0;

        scrollbar-background: $surface 0%;
        scrollbar-background-hover: $surface 0%;
        scrollbar-background-active: $surface 0%;
        scrollbar-color: $surface 50%;
        scrollbar-color-hover: $surface 70%;
        scrollbar-color-active: $surface 100%;

    }
    """

    # background: $surface 50%;
    # border: tall $surface 0%;

    messages = reactive([])  # список объектов сообщений

    def __init__(self, chat_id: UUID):
        super().__init__(id="msg-list")
        self.chat_id = chat_id

    # Жизненный цикл

    async def on_mount(self):
        app_state.messages.sub(self.chat_id, self._messages_cb)
        self._message_widgets: dict[int, Widget] = {}
        self._oldest_msg_id = self.messages[0].local_id
        self._newest_msg_id = self.messages[-1].local_id
        await self._render_all_messages()

    async def on_unmount(self):
        app_state.messages.unsub(self.chat_id, self._messages_cb)

    # Коллбеки

    def _messages_cb(self, messages: list[Message]):
        """Обновление сообщений из message store"""
        self.messages = messages
        self.call_later(self._render_diff_messages)

    # Отрисовки при изменениях

    async def _render_diff_messages(self):
        """Вычисление разницы сообщений, и отрисовка неотрисованных"""
        newer_msgs = [m for m in self.messages if m.local_id > self._newest_msg_id]
        older_msgs = [m for m in self.messages if m.local_id < self._oldest_msg_id]

        if newer_msgs:
            await self._render_newer_diffs(newer_msgs)
            self._newest_msg_id = max([m.local_id for m in newer_msgs])
            self.scroll_end(animate=False)

        if older_msgs:
            await self._render_older_diffs(older_msgs)
            self._oldest_msg_id = min([m.local_id for m in older_msgs])

    async def _render_newer_diffs(self, msgs: list[Message]):
        """Отрисовка новых сообщений"""
        for msg in msgs:
            widget = MessageRowWidget(msg)
            self._message_widgets[msg.local_id] = widget
            await self.mount(widget)

    async def _render_older_diffs(self, msgs: list[Message]):
        """Отрисовка старых сообщений"""
        oldest_widget = self._message_widgets[self._oldest_msg_id]
        for msg in msgs:
            widget = MessageRowWidget(msg)
            self._message_widgets[msg.local_id] = widget
            await self.mount(widget, before=oldest_widget)
            oldest_widget = widget

    async def _render_all_messages(self):
        """Полностью перерисовать список"""
        self.remove_children()
        for msg in self.messages:
            widget = MessageRowWidget(msg)
            self._message_widgets[msg.local_id] = widget
            await self.mount(widget)
        self.scroll_end(animate=False)
