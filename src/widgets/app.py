from textual.app import App, ComposeResult
from textual.containers import Horizontal

from utils.filler import CHAT_IDS
from widgets.active_chat.active_chat import ActiveChatWidget
from widgets.sidebar.sidebar import SidebarWidget


class TapikApp(App[None]):
    """Корневой компонент приложения"""

    BINDINGS = [
        ("d", "toggle_dark", "Toggle dark mode"),
    ]

    def compose(self) -> ComposeResult:
        """Called to add widgets to the app."""
        selected_chat_id = tuple(CHAT_IDS)[3]

        yield Horizontal(
            SidebarWidget(selected_chat_id),
            ActiveChatWidget(selected_chat_id),
        )
