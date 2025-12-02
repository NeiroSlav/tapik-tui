from uuid import UUID

from store.auth import AuthStore
from store.chat import ChatStore
from store.generic import StateStore
from store.message import MessageStore
from store.user import UserStore


class RootStore:

    def __init__(self) -> None:
        self.auth = AuthStore()
        self.users = UserStore()
        self.chats = ChatStore()
        self.messages = MessageStore()

        self.active_chat_id: StateStore[UUID | None] = StateStore(None)
