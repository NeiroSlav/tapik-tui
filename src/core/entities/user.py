from uuid import UUID

from core.entities.base import BaseEntity


class User(BaseEntity):
    user_id: UUID
    username: str
    first_name: str
    last_name: str

    def get_full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    def get_short_name(self) -> str:
        return self.first_name
