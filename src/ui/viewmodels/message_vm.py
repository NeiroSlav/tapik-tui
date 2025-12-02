from core.entities import Message
from store import RootStore


class MessageVM:
    def __init__(self, message: Message, root_store: RootStore):
        self.message = message
        self.root_store = root_store

    @property
    def sender_name(self) -> str:
        if self.message.user_id == self.root_store.current_user_id.get():
            return "Вы"
        user = self.root_store.users.get_user(self.message.user_id)
        return user.get_full_name()

    @property
    def sender_short_name(self) -> str:
        if self.message.user_id == self.root_store.current_user_id.get():
            return "Вы"
        user = self.root_store.users.get_user(self.message.user_id)
        return user.get_short_name()

    @property
    def is_self(self) -> bool:
        return self.message.user_id == self.root_store.current_user_id.get()

    @property
    def str_time(self) -> str:
        return self.message.time.strftime("%H:%M")

    @property
    def full_text(self) -> str:
        return self.message.text
