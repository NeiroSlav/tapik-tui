import random
from datetime import datetime, timedelta

from textual.app import App, ComposeResult
from textual.containers import Horizontal

from core.entities import Message
from widgets.active_chat.active_chat import ActiveChatWidget
from widgets.sidebar.sidebar import SidebarWidget

words = "такие вот слова для сообщения".split()


def generate_text() -> str:
    selected_words = random.choices(words, k=random.randint(2, 20))
    return " ".join(selected_words).capitalize()


messages = [
    Message(
        text=" ".join(random.choices(words, k=random.randint(2, 35))).capitalize(),
        author="Bibus" if i % 3 else "Bobus",
        time=datetime.now() + timedelta(minutes=i),
        is_self=not bool(i % 3),
    )
    for i in range(120)
]


class TapikApp(App[None]):
    """Корневой компонент прилоежния"""

    # CSS_PATH = "tapik.tcss"

    BINDINGS = [
        ("d", "toggle_dark", "Toggle dark mode"),
    ]

    def compose(self) -> ComposeResult:
        """Called to add widgets to the app."""

        yield Horizontal(
            SidebarWidget(),
            ActiveChatWidget(messages),
        )
