from typing import Any

from httpx import AsyncClient, Response

from core.entities import AuthData
from settings import get_settings
from store import RootStore


class ApiError(Exception):
    pass


class BaseClient:
    """
    Базовый клиент для всех api клиентов.
    Автоматически подставляет cookies к запросам.
    При 401 ошибке делает refresh, и пробует снова.
    """

    def __init__(
        self,
        async_client: AsyncClient,
        root_store: RootStore,
    ):
        self.async_client = async_client
        self.root_store = root_store
        self.backend_url = get_settings().backend_url

    def _get_cookies(self) -> dict[str, str]:
        access_token = self.root_store.auth.access_token.get()
        refresh_token = self.root_store.auth.refresh_token.get()
        if access_token and refresh_token:
            return {"access_token": access_token, "refresh_token": refresh_token}
        raise ApiError("No access or refresh token")

    async def _do_refresh(self) -> None:
        response = await self.async_client.post(
            url="/api/auth/refresh",
            cookies=self._get_cookies(),
            headers={"X-Include-Tokens": "true"},
        )
        if not response.is_success:
            raise ApiError(f"Refresh response: {response.status_code}")

        print("SUCCESS", "refresh", response)
        auth_data = AuthData.model_validate(response.json())
        self.root_store.auth.access_token.set(auth_data.access_token)
        self.root_store.auth.refresh_token.set(auth_data.refresh_token)

    def save_cookies(self, auth_data: AuthData):
        self.root_store.auth.access_token.set(auth_data.access_token)
        self.root_store.auth.refresh_token.set(auth_data.refresh_token)

    async def request(
        self,
        method: str,
        url: str,
        json: dict[str, Any] | None = None,
        params: dict[str, str | int | float | bool] | None = None,
        headers: dict[str, str] | None = None,
        add_cookies: bool = True,
        _is_second_try: bool = False,
    ) -> Response:
        cookies = self._get_cookies() if add_cookies else None
        response = await self.async_client.request(
            method=method,
            url=url,
            json=json,
            params=params,
            headers=headers,
            cookies=cookies,
        )

        if response.is_success:
            return response

        if response.status_code == 401 and not _is_second_try:
            await self._do_refresh()
            return await self.request(
                method=method,
                url=url,
                json=json,
                params=params,
                headers=headers,
                add_cookies=add_cookies,
                _is_second_try=True,
            )

        raise ApiError(f"Request '{url}' failed: {response.status_code}")
