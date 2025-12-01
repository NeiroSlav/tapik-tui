from typing import Callable, TypeAlias
from uuid import UUID

from core.entities import Chat, Message
from utils.filler import chats

ChatSubscriberCB: TypeAlias = Callable[[list[Chat]], None]


class ChatStore:
    """Хранилище чатов с подпиской на изменения."""

    def __init__(self):
        self._chats: dict[UUID, Chat] = chats
        self._subs: list[ChatSubscriberCB] = []

    def add_chat(self, chat: Chat):
        """Добавление сообщения"""
        self._chats[chat.chat_id] = chat
        self._notify_subscribers()

    def upd_last_msg(self, chat_id: UUID, msg: Message):
        """Обновление последнего сообщения в чате"""
        if chat := self._chats.get(chat_id):
            chat.last_msg = msg
            self._notify_subscribers()

    def get_chat(self, chat_id: UUID) -> Chat:
        """Ищет чат по id"""
        return self._chats[chat_id]

    def sub(self, callback: ChatSubscriberCB):
        """Подписка виджетов на обновления"""
        self._subs.append(callback)
        callback(self._get_sorted_chats())

    def unsub(self, callback: ChatSubscriberCB):
        """Отписка виджетов от обновления"""
        self._subs.remove(callback)

    def _notify_subscribers(self):
        chats = self._get_sorted_chats()
        for cb in self._subs:
            cb(chats)

    def _get_sorted_chats(self) -> list[Chat]:
        return sorted(
            self._chats.values(),
            key=lambda c: c.last_msg.time,
            reverse=True,
        )
