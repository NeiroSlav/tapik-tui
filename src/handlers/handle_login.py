from store.app_state import app_state


async def handle_login(username: str, password: str):
    users = [u for u in app_state.users.get_users() if u.username == username]
    if not users:
        return

    app_state.current_user_id.set(users[0].user_id)
