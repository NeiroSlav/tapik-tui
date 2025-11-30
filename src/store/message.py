from typing import Callable, Coroutine, TypeAlias

from core.entities import Message
from utils.filler import messages
from utils.logger import logger

MsgSubscriberCB: TypeAlias = Callable[[list[Message]], Coroutine[None, None, None]]


class MessageStore:
    """Хранилище сообщений с подпиской на изменения."""

    def __init__(self):
        self._messages: list[Message] = messages
        self._subscribers: list[MsgSubscriberCB] = []

    @property
    def messages(self):
        return self._messages

    async def add_message(self, msg: Message):
        """Добавление сообщения"""
        self._messages.append(msg)
        self._messages.sort(key=lambda m: m.local_id)
        logger(f"New message: {msg.text}")
        await self._notify_subscribers()

    def subscribe(self, callback: MsgSubscriberCB):
        """Подписка виджетов на обновления"""
        self._subscribers.append(callback)

    async def _notify_subscribers(self):
        for cb in self._subscribers:
            await cb(self._messages)

    def test_get_first_id(self) -> int:
        return self.messages[0].local_id

    def test_get_last_id(self) -> int:
        return self.messages[-1].local_id


message_store = MessageStore()
