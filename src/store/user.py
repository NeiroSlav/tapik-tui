from collections import defaultdict
from typing import Callable, TypeAlias
from uuid import UUID

from core.entities import User
from utils.filler import users

UserSubscriberCB: TypeAlias = Callable[[User], None]


class UserStore:
    """Хранилище юзеров с подпиской на изменения."""

    def __init__(self):
        self._users: dict[UUID, User] = users
        self._subs: dict[UUID, list[UserSubscriberCB]] = defaultdict(list)

    def set_user(self, user: User):
        """Добавление юзера"""
        self._users[user.user_id] = user
        self._notify_subscribers(user.user_id)

    def get_user(self, user_id: UUID) -> User:
        """Ищет юзера по id"""
        return self._users[user_id]

    def get_users(self) -> list[User]:
        """Отдаёт список всех юзеров"""
        return [*self._users.values()]

    def sub(self, user_id: UUID, callback: UserSubscriberCB):
        """Подписка виджетов на обновления"""
        self._subs[user_id].append(callback)
        callback(self._users[user_id])

    def unsub(self, user_id: UUID, callback: UserSubscriberCB):
        """Отписка виджетов от обновления"""
        self._subs[user_id].remove(callback)

    def _notify_subscribers(self, user_id: UUID):
        for cb in self._subs[user_id]:
            cb(self._users[user_id])
