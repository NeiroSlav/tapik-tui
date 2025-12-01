from uuid import UUID

from textual.containers import VerticalScroll
from textual.reactive import reactive

from core.entities import Chat
from store.app_state import app_state
from store.chat import chat_store
from utils.logger import logger
from widgets.sidebar.chat_preview import ChatPreviewWidget


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

    def __init__(self):
        super().__init__()

        self.chats = chat_store.get_sorted_chats()
        chat_store.subscribe(self._subscibe_cb)

        self.selected_chat_id = app_state.active_chat_id.get()
        app_state.active_chat_id.subscribe(self._chat_id_cb)

    def _chat_id_cb(self, chat_id: UUID | None):
        self.selected_chat_id = chat_id

    def watch_selected_chat_id(self, chat_id: UUID | None):
        """Перерисовка всех виджетов с новым chat_id"""
        self.call_next(self._render_all_chats)

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
            is_selected = chat.chat_id == self.selected_chat_id
            widget = ChatPreviewWidget(chat, is_selected)
            await self.mount(widget)
