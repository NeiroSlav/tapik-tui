from core.entities import Chat
from store import RootStore
from ui.viewmodels.message_vm import MessageVM


class ChatVM:
    def __init__(self, chat: Chat, root_store: RootStore):
        self.chat = chat
        self.root_store = root_store
        self.message_vm = MessageVM(chat.last_msg, root_store)

    @property
    def name(self) -> str:
        return self.chat.name
