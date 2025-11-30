from collections import defaultdict
from typing import Callable, Coroutine, TypeAlias
from uuid import UUID

from core.entities import Message
from utils.filler import messages
from utils.logger import logger

MsgSubscriberCB: TypeAlias = Callable[[list[Message]], Coroutine[None, None, None]]


class MessageStore:
    """Хранилище сообщений с подпиской на изменения."""

    def __init__(self):
        self._messages: dict[UUID, list[Message]] = messages
        self._subscribers: dict[UUID, list[MsgSubscriberCB]] = defaultdict(list)

    def get_chat_messages(self, chat_id: UUID):
        return self._messages[chat_id]

    async def add_messages(self, msgs: list[Message]):
        """Добавление сообщения"""
        updated_chat_ids: set[UUID] = set()
        for msg in msgs:
            self._messages[msg.chat_id].append(msg)
            updated_chat_ids.add(msg.chat_id)
            logger(f"New message: {msg.text}")

        for chat_id in updated_chat_ids:
            self._messages[chat_id].sort(key=lambda m: m.local_id)

        await self._notify_subscribers(updated_chat_ids)

    def subscribe(self, chat_id: UUID, callback: MsgSubscriberCB):
        """Подписка виджетов на обновления"""
        self._subscribers[chat_id].append(callback)

    async def _notify_subscribers(self, chat_ids: set[UUID]):
        for chat_id in chat_ids:
            for cb in self._subscribers[chat_id]:
                await cb(self._messages[chat_id])

    def test_get_first_id(self, chat_id: UUID) -> int:
        return self._messages[chat_id][0].local_id

    def test_get_last_id(self, chat_id: UUID) -> int:
        return self._messages[chat_id][-1].local_id


message_store = MessageStore()
