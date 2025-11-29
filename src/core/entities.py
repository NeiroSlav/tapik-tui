from dataclasses import dataclass
from datetime import datetime


@dataclass
class Message:
    text: str
    author: str
    time: datetime
    is_self: bool
