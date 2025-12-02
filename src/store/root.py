from uuid import UUID

from store.chat import ChatStore
from store.generic import StateStore
from store.message import MessageStore
from store.user import UserStore


class RootStore:

    def __init__(self) -> None:
        self.users = UserStore()
        self.chats = ChatStore()
        self.messages = MessageStore()

        self.active_chat_id: StateStore[UUID | None] = StateStore(None)
        self.current_user_id: StateStore[UUID | None] = StateStore(None)

    def current_user_id_strict(self) -> UUID:
        user_id = self.current_user_id.get()
        if not user_id:
            raise ValueError("No current user id")
        return user_id
