from textual.app import App, ComposeResult
from textual.containers import Horizontal

from utils.filler import CHAT_IDS
from widgets.active_chat.active_chat import ActiveChatWidget
from widgets.sidebar.sidebar import SidebarWidget


class TapikApp(App[None]):
    """Корневой компонент прилоежния"""

    BINDINGS = [
        ("d", "toggle_dark", "Toggle dark mode"),
    ]

    def compose(self) -> ComposeResult:
        """Called to add widgets to the app."""

        yield Horizontal(
            SidebarWidget(),
            ActiveChatWidget(tuple(CHAT_IDS)[0]),
        )
