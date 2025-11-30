import random
from datetime import datetime, timedelta
from uuid import UUID, uuid4

from core.entities import Chat, Message

msg_words = "такие вот слова для сообщения".split()
chat_words = "просто чат группа наше".split()


def generate_text() -> str:
    selected_words = random.choices(msg_words, k=random.randint(2, 20))
    return " ".join(selected_words).capitalize()


def generate_name() -> str:
    selected_words = random.choices(chat_words, k=3)
    return " ".join(selected_words).capitalize()


def create_messages(chat_id: UUID) -> list[Message]:
    return [
        Message(
            local_id=i + 20,
            chat_id=chat_id,
            text=generate_text(),
            author="Bibus" if i % 3 else "Bobus",
            time=datetime.now() + timedelta(minutes=i),
            is_self=not bool(i % 3),
        )
        for i in range(20)
    ]


CHAT_IDS = set(uuid4() for _ in range(20))


messages: dict[UUID, list[Message]] = {
    chat_id: create_messages(chat_id) for chat_id in CHAT_IDS
}

chats: dict[UUID, Chat] = {
    chat_id: Chat(
        name=generate_name(),
        chat_id=chat_id,
        last_msg=messages[chat_id][-1],
    )
    for chat_id in CHAT_IDS
}
