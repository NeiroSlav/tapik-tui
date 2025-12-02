import random
from datetime import datetime, timedelta
from uuid import UUID, uuid4

from core.entities import Chat, Message, User

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
            user_id=random.choice(_user_ids),
            text=generate_text(),
            time=datetime.now() + timedelta(minutes=i - 30),
        )
        for i in range(20)
    ]


first_names = "Иван Богдан Артём Григорий Женя".split()
last_names = "Желебев Попов Селезнёв Джиджа Немцов".split()
USERNAMES = "neiroslav jjake urii shampun qrabbit".split()

CHAT_IDS = set(uuid4() for _ in range(20))


_users: list[User] = [
    User(
        user_id=uuid4(),
        username=username,
        first_name=first_names[i],
        last_name=last_names[i],
    )
    for i, username in enumerate(USERNAMES)
]

users: dict[UUID, User] = {u.user_id: u for u in _users}

_user_ids: tuple[UUID, ...] = tuple(users.keys())

current_user_id = _user_ids[0]

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
