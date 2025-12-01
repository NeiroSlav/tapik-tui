from uuid import UUID

from store.chat import ChatStore
from store.generic import StateStore
from store.message import MessageStore
from store.user import UserStore
from utils.filler import current_user_id


class MainAppStore:

    def __init__(self) -> None:
        self.users = UserStore()
        self.chats = ChatStore()
        self.messages = MessageStore()

        self.active_chat_id: StateStore[UUID | None] = StateStore(None)
        self.current_user_id = current_user_id


app_state = MainAppStore()
