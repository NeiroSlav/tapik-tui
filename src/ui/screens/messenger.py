from contextlib import suppress

from textual.app import ComposeResult
from textual.containers import Horizontal
from textual.screen import Screen

from ui.root_mixin import RootProviderMixin
from ui.widgets.active_chat.active_chat import ActiveChatWidget
from ui.widgets.chat_list.chat_list import SidebarWidget


class MessengerScreen(Screen[None], RootProviderMixin):

    def compose(self) -> ComposeResult:
        """Called to add widgets to the app."""

        yield Horizontal(
            SidebarWidget(),
            ActiveChatWidget(),
        )

    # Хендлеры клавиш

    BINDINGS = [
        ("h", "focus_chat_list"),
        ("l", "focus_msg_list"),
        #
        ("H", "focus_chat_list"),
        ("L", "focus_msg_list"),
        #
        ("i", "enter_input"),
        ("escape", "exit_input"),
    ]

    # Фокусировки

    def action_focus_chat_list(self):
        self.query_one("#chat-list").focus()

    def action_focus_msg_list(self):
        with suppress(Exception):
            self.query_one("#msg-list").focus()
            self.query_one(
                "#chat-list",
                SidebarWidget,
            ).cursor_chat_id = None

    # Поле ввода сообщения

    def action_enter_input(self):
        with suppress(Exception):
            self.query_one("#msg-input").focus()

    def action_exit_input(self):
        with suppress(Exception):
            self.query_one("#msg-list").focus()
