from uuid import UUID

from httpx import AsyncClient

from controller.base import BaseResponse
from settings import get_settings
from store import RootStore


class AuthResponse(BaseResponse):
    user_id: UUID
    session_id: UUID
    access_token: str
    refresh_token: str


class AuthController:

    def __init__(self, root_store: RootStore) -> None:
        self.root_store = root_store
        self.backend_url = get_settings().backend_url

    async def login(self, username: str, password: str) -> AuthResponse:
        async with AsyncClient() as client:
            response = await client.post(
                f"{self.backend_url}/api/auth/login",
                json={
                    "username": username,
                    "password": password,
                },
                headers={"X-Include-Tokens": "true"},
            )
            return AuthResponse.model_validate(response.json())

    async def refresh(self) -> AuthResponse:
        async with AsyncClient() as client:
            response = await client.post(
                f"{self.backend_url}/api/auth/refresh",
                headers={"X-Include-Tokens": "true"},
            )
            return AuthResponse.model_validate(response.json())
