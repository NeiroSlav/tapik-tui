from uuid import UUID

from store.generic import StateStore


class AuthStore:

    def __init__(self) -> None:
        self.access_token: StateStore[str | None] = StateStore(None)
        self.refresh_token: StateStore[str | None] = StateStore(None)
        self.current_user_id: StateStore[UUID | None] = StateStore(None)

    def set_tokens(self, access: str, refresh: str):
        self.access_token.set(access)
        self.refresh_token.set(refresh)

    def clear(self):
        self.access_token.set(None)
        self.refresh_token.set(None)

    def get_user_id_strict(self) -> UUID:
        user_id = self.current_user_id.get()
        if not user_id:
            raise ValueError("No current user id")
        return user_id
