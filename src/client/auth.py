from client.base import BaseClient
from core.entities import AuthData


class AuthClient(BaseClient):

    async def login(self, username: str, password: str) -> None:
        response = await self.request(
            method="POST",
            url="/api/auth/login",
            json={"username": username, "password": password},
            headers={"X-Include-Tokens": "true"},
            add_cookies=False,
        )
        auth_data = AuthData.model_validate(response.json())
        self.save_cookies(auth_data)
        self.root_store.auth.current_user_id.set(auth_data.user_id)

    async def logout(self) -> None:
        await self.request(method="POST", url="/api/auth/logout")
        self.root_store.auth.current_user_id.set(None)
