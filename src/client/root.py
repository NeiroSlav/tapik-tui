from httpx import AsyncClient

from client.auth import AuthClient
from client.chat import ChatClient
from settings import get_settings
from store.root import RootStore


class RootClient:

    def __init__(self, root_store: RootStore) -> None:
        self._client = AsyncClient(base_url=get_settings().backend_url)
        self.auth = AuthClient(self._client, root_store)
        self.chat = ChatClient(self._client, root_store)

    async def close(self):
        await self._client.aclose()
