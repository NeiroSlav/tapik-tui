from uuid import UUID

from textual.containers import VerticalScroll
from textual.reactive import reactive

from core.entities import Chat
from store.chat import chat_store
from utils.logger import logger
from widgets.sidebar.chat import ChatWidget


class SidebarWidget(VerticalScroll):
    """Список чатов."""

    DEFAULT_CSS = """
    SidebarWidget {
        width: 30%;
        height: 100%;
        padding: 0 0;
    }
    """

    chats = reactive([])  # список объектов сообщений
    selected_chat_id = reactive(None)

    def __init__(self, selected_chat_id: UUID):
        super().__init__()
        self.chats = chat_store.get_chats()
        self.selected_chat_id = selected_chat_id
        chat_store.subscribe(self._subscibe_cb)

    # Отрисовки при изменении

    def _subscibe_cb(self, chats: list[Chat]):
        """Коллбек обновления для интеграции в chats store"""
        logger("Коллбек отработал")
        self.chats = chats
        self.call_after_refresh(self._render_all_chats)

    # Отрисовки при монтировании

    async def on_mount(self):
        """Действия при монтировании"""
        await self._render_all_chats()

    async def _render_all_chats(self):
        """Полностью перерисовать список."""
        self.remove_children()
        for chat in self.chats:
            widget = ChatWidget(chat, chat.chat_id == self.selected_chat_id)
            await self.mount(widget)
