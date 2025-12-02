from uuid import UUID

from store.chat import ChatStore
from store.generic import StateStore
from store.message import MessageStore
from store.user import UserStore


class RootStore:

    def __init__(self, current_user_id: UUID) -> None:
        self.users = UserStore()
        self.chats = ChatStore()
        self.messages = MessageStore()

        self.active_chat_id: StateStore[UUID | None] = StateStore(None)
        self.current_user_id: StateStore[UUID] = StateStore(current_user_id)
