from typing import Callable, Generic, TypeAlias, TypeVar

T = TypeVar("T")
SubCallback: TypeAlias = Callable[[T], None]


class StateStore(Generic[T]):
    """
    Хранилище состояния с возможность подписываться на обновления.
    """

    def __init__(self, default: T):
        self._state = default
        self._subs: list[SubCallback[T]] = []

    def set(self, state: T):
        """Установка значения"""
        self._state = state
        self._notify_subscribers()

    def get(self) -> T:
        """Получение значения"""
        return self._state

    def subscribe(self, callback: SubCallback[T]):
        """Подписка на состояние"""
        self._subs.append(callback)

    def unsubscribe(self, callback: SubCallback[T]):
        """Отписка от состояния"""
        self._subs.remove(callback)

    def _notify_subscribers(self):
        """Оповещение подписчиков"""
        for cb in self._subs:
            cb(self._state)
