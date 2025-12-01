from uuid import UUID

from store.generic import StateStore


class MainAppState:

    def __init__(self) -> None:
        self.active_chat_id: StateStore[UUID | None] = StateStore(None)


app_state = MainAppState()
