from typing import Callable, TypeAlias
from uuid import UUID

from core.entities import Chat, Message
from utils.filler import chats

ChatSubscriberCB: TypeAlias = Callable[[list[Chat]], None]


class ChatStore:
    """Хранилище чатов с подпиской на изменения."""

    def __init__(self):
        self._chats: dict[UUID, Chat] = chats
        self._subscribers: list[ChatSubscriberCB] = []

    @property
    def chats(self):
        return self._chats

    def add_chat(self, chat: Chat):
        """Добавление сообщения"""
        self._chats[chat.chat_id] = chat
        self._notify_subscribers()

    def upd_last_msg(self, chat_id: UUID, msg: Message):
        """Обновление последнего сообщения в чате"""
        if chat := self._chats.get(chat_id):
            chat.last_msg = msg
            self._notify_subscribers()

    def subscribe(self, callback: ChatSubscriberCB):
        """Подписка виджетов на обновления"""
        self._subscribers.append(callback)

    def _notify_subscribers(self):
        chats = self.get_chats()
        for cb in self._subscribers:
            cb(chats)

    def get_chats(self) -> list[Chat]:
        return sorted(self._chats.values(), key=lambda c: c.last_msg.time)


chat_store = ChatStore()
