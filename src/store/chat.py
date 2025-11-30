# from typing import Callable, Coroutine, TypeAlias

# from core.entities import Chat
# from utils.filler import chats
# from utils.logger import logger

# MsgSubscriberCB: TypeAlias = Callable[[list[Chat]], Coroutine[None, None, None]]


# class ChatStore:
#     """Хранилище сообщений с подпиской на изменения."""

#     def __init__(self):
#         self._chats: list[Chat] = chats
#         self._subscribers: list[MsgSubscriberCB] = []

#     @property
#     def chats(self):
#         return self._chats

#     async def add_chat(self, msg: Chat):
#         """Добавление сообщения"""
#         self._chats.append(msg)
#         self._chats.sort(key=lambda m: m.local_id)
#         logger(f"New chat: {msg.text}")
#         await self._notify_subscribers()

#     def subscribe(self, callback: MsgSubscriberCB):
#         """Подписка виджетов на обновления"""
#         self._subscribers.append(callback)

#     async def _notify_subscribers(self):
#         for cb in self._subscribers:
#             await cb(self._chats)

#     def test_get_first_id(self) -> int:
#         return self.chats[0].local_id

#     def test_get_last_id(self) -> int:
#         return self.chats[-1].local_id


# chat_store = ChatStore()
