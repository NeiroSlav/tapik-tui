from uuid import UUID

from core.entities.base import BaseEntity
from core.entities.message import Message


class Chat(BaseEntity):
    name: str
    chat_id: UUID
    last_message: Message
