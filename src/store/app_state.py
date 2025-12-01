from uuid import UUID

from store.chat import ChatStore
from store.generic import StateStore
from store.message import MessageStore


class MainAppStore:

    def __init__(self) -> None:
        self.chats: ChatStore = ChatStore()
        self.messages: MessageStore = MessageStore()

        self.active_chat_id: StateStore[UUID | None] = StateStore(None)


app_state = MainAppStore()
