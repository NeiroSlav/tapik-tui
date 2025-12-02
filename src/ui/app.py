from textual.app import App

# from ui.screens.login import LoginScreen
from ui.screens.messenger import MessengerScreen
from utils.filler import current_user_id


class TapikApp(App[None]):
    """Корневой компонент приложения"""

    async def on_mount(self):
        # await self.mount(LoginScreen())
        await self.mount(MessengerScreen(current_user_id=current_user_id))
