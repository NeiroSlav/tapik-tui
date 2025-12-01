from textual.app import App

# from ui.screens.login import LoginScreen
from ui.screens.messenger import MessengerScreen


class TapikApp(App[None]):
    """Корневой компонент приложения"""

    async def on_mount(self):
        # await self.mount(LoginScreen())
        await self.mount(MessengerScreen())
