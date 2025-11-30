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
        msg.local_id = len(self.messages)
        self._messages.append(msg)
        self._notify_subscribers()
        logger(f"New message: {msg.text}")

    def subscribe(self, callback: MsgSubscriberCB):
        """Подписка виджетов на обновления"""
        self._subscribers.append(callback)

    def _notify_subscribers(self):
        for cb in self._subscribers:
            cb(self._messages)

    # def test_get_first_id(self) -> int:
    #     return self.messages[0].local_id

    # def test_get_last_id(self) -> int:
    #     return self.messages[-1].local_id


message_store = MessageStore()
