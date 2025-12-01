from core.entities import Message
from store.app_state import app_state


def get_sender_name(message: Message, full: bool = False) -> str:
    if message.user_id == app_state.current_user_id:
        return "Вы"

    sender = app_state.users.get_user(message.user_id)
    if full:
        return sender.get_full_name()
    return sender.get_short_name()


def is_self_message(message: Message) -> bool:
    return message.user_id == app_state.current_user_id
