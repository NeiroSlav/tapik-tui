from uuid import UUID

from textual.containers import Vertical

from store.app_state import app_state
from ui.widgets.active_chat.chat_header import ChatHeaderWidget
from ui.widgets.active_chat.msg_input import MessageInputWidget
from ui.widgets.active_chat.msg_list.msg_list import MessageListWidget


class ActiveChatWidget(Vertical):
    """Активный чат."""

    chat_id: UUID | None = None

    # Жизненный цикл

    async def on_mount(self):
        app_state.active_chat_id.sub(self._chat_id_cb)
        await self._render_active_chat()

    async def on_unmount(self):
        app_state.active_chat_id.unsub(self._chat_id_cb)

    # Коллбеки

    def _chat_id_cb(self, chat_id: UUID | None):
        """Обновление сообщений из app state"""
        self.chat_id = chat_id
        self.call_next(self._render_active_chat)

    # Отрисовка

    async def _render_active_chat(self):
        """Отрисовать все виджеты чат"""
        self.remove_children()
        if not self.chat_id:
            return

        await self.mount(ChatHeaderWidget(self.chat_id))
        await self.mount(MessageInputWidget(self.chat_id))
        await self.mount(MessageListWidget(self.chat_id))

    # Хендлеры клавиш

    BINDINGS = [
        ("k", "scroll_up"),
        ("j", "scroll_down"),
        #
        ("K", "scroll_page_up"),
        ("J", "scroll_page_down"),
        #
        ("ctrl+k", "scroll_page_up"),
        ("ctrl+j", "scroll_page_down"),
        #
        ("ctrl+u", "scroll_page_up"),
        ("ctrl+d", "scroll_page_down"),
    ]

    # Сильные прокрутки

    def action_scroll_page_up(self):
        self.query_one("#msg-list").scroll_page_up()

    def action_scroll_page_down(self):
        self.query_one("#msg-list").scroll_page_down()

    # Слабая прокрутка

    def action_scroll_up(self):
        self.query_one("#msg-list").scroll_up()

    def action_scroll_down(self):
        self.query_one("#msg-list").scroll_down()
