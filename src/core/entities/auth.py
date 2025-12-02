from uuid import UUID

from core.entities.base import BaseEntity


class AuthData(BaseEntity):
    user_id: UUID
    session_id: UUID
    access_token: str
    refresh_token: str
