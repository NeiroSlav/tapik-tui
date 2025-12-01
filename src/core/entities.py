from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class Message:
    local_id: int
    chat_id: UUID
    user_id: UUID
    text: str
    time: datetime


@dataclass
class Chat:
    name: str
    chat_id: UUID
    last_msg: Message


@dataclass
class User:
    user_id: UUID
    username: str
    first_name: str
    last_name: str

    def get_full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    def get_short_name(self) -> str:
        return self.first_name
