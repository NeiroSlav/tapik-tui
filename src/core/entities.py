from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class Message:
    local_id: int
    chat_id: UUID
    text: str
    author: str
    time: datetime
    is_self: bool


@dataclass
class Chat:
    name: str
    chat_id: UUID
    last_msg: Message
