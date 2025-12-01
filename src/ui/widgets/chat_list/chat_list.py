from uuid import UUID

from textual.containers import VerticalScroll
from textual.reactive import reactive

from core.entities import Chat
from store.app_state import app_state
from ui.widgets.chat_list.chat_preview import ChatPreviewWidget


class SidebarWidget(VerticalScroll):
    """Список чатов."""

    DEFAULT_CSS = """
    SidebarWidget {
        width: 30%;
        height: 100%;
        padding: 0 0;

        scrollbar-background: $surface 0%;
        scrollbar-background-hover: $surface 0%;
        scrollbar-background-active: $surface 0%;
        scrollbar-color: $surface 50%;
        scrollbar-color-hover: $surface 70%;
        scrollbar-color-active: $surface 100%;
    }
    """

    cursor_chat_id = reactive(None)

    def __init__(self):
        super().__init__(id="chat-list")

        self.chats: list[Chat] = []
        self.active_chat_id: UUID | None = None
        self.cursor_chat_id = None

    # Жизненный цикл

    async def on_mount(self):
        app_state.chats.sub(self._chats_cb)
        app_state.active_chat_id.sub(self._active_chat_id_cb)
        await self._render_all_chats()

    async def on_unmount(self):
        app_state.chats.unsub(self._chats_cb)
        app_state.active_chat_id.unsub(self._active_chat_id_cb)

    # Коллбеки

    def watch_cursor_chat_id(self):
        self.call_after_refresh(self._render_all_chats)

    def _active_chat_id_cb(self, chat_id: UUID | None):
        """Коллбек обновления active_chat_id из state"""
        self.active_chat_id = chat_id
        self.call_after_refresh(self._render_all_chats)

    def _chats_cb(self, chats: list[Chat]):
        """Коллбек обновления chats из state"""
        self.chats = chats
        self.call_after_refresh(self._render_all_chats)

    def _on_chat_click_cb(self, chat_id: UUID):
        """Коллбек установки active_chat_id в state из виджета чата"""
        app_state.active_chat_id.set(chat_id)
        self.cursor_chat_id = chat_id

    # Отрисовка

    async def _render_all_chats(self):
        """Полностью перерисовать список."""
        self.remove_children()
        for chat in self.chats:
            widget = ChatPreviewWidget(
                chat=chat,
                is_active=chat.chat_id == self.active_chat_id,
                is_cursor=chat.chat_id == self.cursor_chat_id,
                on_chat_click=self._on_chat_click_cb,
            )
            await self.mount(widget)

    # Хендлеры клавиш

    BINDINGS = [
        ("k", "select_prev"),
        ("j", "select_next"),
        #
        ("K", "select_prev_jump"),
        ("J", "select_next_jump"),
        #
        ("ctrl+k", "set_prev"),
        ("ctrl+j", "set_next"),
        #
        ("enter", "set_selected"),
    ]

    # Работа с курсором

    def action_select_next(self):
        self._set_new_cursor_chat_id(1)

    def action_select_prev(self):
        self._set_new_cursor_chat_id(-1)

    def action_set_next(self):
        self._set_new_cursor_chat_id(1)
        app_state.active_chat_id.set(self.cursor_chat_id)

    def action_set_prev(self):
        self._set_new_cursor_chat_id(-1)
        app_state.active_chat_id.set(self.cursor_chat_id)

    def action_select_next_jump(self):
        self._set_new_cursor_chat_id(5)

    def action_select_prev_jump(self):
        self._set_new_cursor_chat_id(-5)

    def action_set_selected(self):
        app_state.active_chat_id.set(self.cursor_chat_id)

    # Утилиты курсора

    def _get_cursor_id(self) -> UUID:
        """Получает chat_id курсора"""
        if self.cursor_chat_id:  # Если он есть - отдаём его
            return self.cursor_chat_id
        if self.active_chat_id:  # Если есть активный чат - отдаём его
            return self.active_chat_id
        return self.chats[0].chat_id  # Отдаём id первого чата

    def _set_new_cursor_chat_id(self, index_shift: int):
        """Установка нового курсора"""
        chat_ids = list(map(lambda c: c.chat_id, self.chats))
        current_index = chat_ids.index(self._get_cursor_id())
        new_index = current_index + index_shift
        if new_index < 0:
            new_index = 0
        if new_index >= len(chat_ids):
            new_index = len(chat_ids) - 1
        self.cursor_chat_id = chat_ids[new_index]
        self._scroll_to_cursor()

    def _scroll_to_cursor(self):
        """Прокрутить список так, чтобы чат, на котором курсор - был виден"""
        if self.cursor_chat_id is None:
            return

        # поиск виджета по chat_id
        for widget in self.children:
            if isinstance(widget, ChatPreviewWidget):
                if widget.chat.chat_id == self.cursor_chat_id:
                    return self.scroll_to_widget(widget)
