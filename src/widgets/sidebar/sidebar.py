from textual.containers import Vertical
from textual.reactive import reactive


class SidebarWidget(Vertical):
    """Список чатов."""

    DEFAULT_CSS = """
    SidebarWidget {
        width: 30%;
        height: 100%;
        padding: 0 0;
    }
    """

    chats = reactive([])  # список объектов сообщений

    def __init__(self):
        super().__init__()
        self.chats = []

    async def on_mount(self):
        await self.render_messages()

    async def render_messages(self):
        """Полностью перерисовать список."""
        self.remove_children()

        # for chat in self.messages:
        #     widget = MessageRowWidget(msg)
        #     await self.mount(widget)

        # self.scroll_end(animate=False)

    # async def add_message(self, msg: Message):
    #     """Добавить одно сообщение и отрендерить его."""
    #     self.messages = self.messages + [msg]  # триггерит reactive
    #     self.messages = self.messages + [msg]  # триггерит reactive
