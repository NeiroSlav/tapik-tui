from uuid import UUID

from textual.app import App

from actions.root import RootActions
from store import RootStore
from ui.screens.login import LoginScreen
from ui.screens.messenger import MessengerScreen


class TapikApp(App[None]):
    """Корневой компонент приложения"""

    current_user_id: UUID | None = None

    def __init__(self):
        super().__init__()
        self.root_store = RootStore()
        self.root_actions = RootActions(self.root_store)
        self.root_store.auth.current_user_id.sub(self._current_user_id_cb)

    def _current_user_id_cb(self, current_user_id: UUID | None):
        self.current_user_id = current_user_id
        self.call_next(self._set_needed_screen)

    async def on_mount(self):
        self.install_screen(  # type: ignore
            screen=LoginScreen(),
            name="login",
        )
        self.install_screen(  # type: ignore
            screen=MessengerScreen(),
            name="messenger",
        )
        await self._set_needed_screen()

    async def _set_needed_screen(self) -> None:
        screen_name = "login" if not self.current_user_id else "messenger"
        await self.push_screen(screen_name)  # type: ignore
