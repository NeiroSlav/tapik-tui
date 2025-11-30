import random
from datetime import datetime, timedelta

from core.entities import Message

words = "такие вот слова для сообщения".split()


def generate_text() -> str:
    selected_words = random.choices(words, k=random.randint(2, 20))
    return " ".join(selected_words).capitalize()


messages = [
    Message(
        text=" ".join(random.choices(words, k=random.randint(2, 35))).capitalize(),
        author="Bibus" if i % 3 else "Bobus",
        time=datetime.now() + timedelta(minutes=i),
        is_self=not bool(i % 3),
        local_id=i + 20,
    )
    for i in range(20)
]
