from typing import Callable, TypeAlias

from core.entities import Message
from utils.filler import messages
from utils.logger import logger

MsgSubscriberCB: TypeAlias = Callable[[list[Message]], None]


class MessageStore:
    """Хранилище сообщений с подпиской на изменения."""

    def __init__(self):
        self._messages: list[Message] = messages
        self._subscribers: list[MsgSubscriberCB] = []

    @property
    def messages(self):
        return self._messages

    def add_message(self, msg: Message):
        self._messages.append(msg)
        self._notify_subscribers()
        logger(f"New message: {msg.text}")

    def subscribe(self, callback: MsgSubscriberCB):
        """Подписка виджетов на обновления"""
        self._subscribers.append(callback)

    def _notify_subscribers(self):
        for cb in self._subscribers:
            cb(self._messages)


message_store = MessageStore()
