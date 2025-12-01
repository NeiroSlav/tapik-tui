from uuid import UUID

from textual.containers import Vertical
from textual.events import Mount
from textual.reactive import reactive
from textual.widget import Widget

from store.app_state import app_state
from widgets.active_chat.chat_header import ChatHeaderWidget
from widgets.active_chat.msg_input import MessageInputWidget
from widgets.active_chat.msg_list.msg_list import MessageListWidget


class InactiveChatWidget(Widget):
    def render(self):
        return "Выберите чат"


class ActiveChatWidget(Vertical):
    """Активный чат."""

    chat_id = reactive(None)

    def __init__(self):
        super().__init__()
        self.chat_id = app_state.active_chat_id.get()
        app_state.active_chat_id.subscribe(self._chat_id_cb)

    def _chat_id_cb(self, chat_id: UUID | None):
        self.chat_id = chat_id

    async def watch_chat_id(self, chat_id: UUID | None):
        """Перерисовка всех виджетов с новым chat_id"""
        self.call_next(self._render_active_chat)

    async def on_mount(self, event: Mount) -> None:
        """Действия при монтировании"""
        await self._render_active_chat()

    async def _render_active_chat(self):
        """Отрисовать все виджеты чат"""
        self.remove_children()

        if not self.chat_id:
            return await self.mount(InactiveChatWidget())

        await self.mount(ChatHeaderWidget(self.chat_id))
        await self.mount(MessageInputWidget(self.chat_id))
        await self.mount(MessageListWidget(self.chat_id))
