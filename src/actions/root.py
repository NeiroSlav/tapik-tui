from datetime import datetime
from uuid import UUID

from core.entities import Message
from store.root import RootStore


class RootActions:

    def __init__(self, root_store: RootStore) -> None:
        self.root_store = root_store

    def login(self, username: str, password: str):
        users = [u for u in self.root_store.users.get_users() if u.username == username]
        if not users:
            return

        self.root_store.current_user_id.set(users[0].user_id)

    def select_chat(self, chat_id: UUID):
        self.root_store.active_chat_id.set(chat_id)

    def send_message(self, chat_id: UUID, text: str):
        message = Message(
            text=text,
            user_id=self.root_store.current_user_id_strict(),
            time=datetime.now(),
            local_id=self.root_store.messages.test_get_last_id(chat_id) + 1,
            chat_id=chat_id,
        )
        self.root_store.messages.add_messages([message])
        self.root_store.chats.upd_last_msg(chat_id, message)

    # def _post_old_msg(self, text: str) -> None:
    #     self.root_store.messages.add_messages(
    #         [
    #             Message(
    #                 text=text,
    #                 user_id=self.root_store.current_user_id_strict(),
    #                 time=datetime.now(),
    #                 local_id=self.root_store.messages.test_get_first_id(self.chat_id)
    #                 - 1,
    #                 chat_id=self.chat_id,
    #             )
    #         ]
    #     )
