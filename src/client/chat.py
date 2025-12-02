from client.base import BaseClient
from core.entities import Chat


class ChatClient(BaseClient):

    async def list_by_user(self, offset: int) -> list[Chat]:
        response = await self.request(
            method="GET",
            url="/api/chats/",
            params={"offset": offset},
        )
        chats = [Chat.model_validate(c) for c in response.json()]
        self.root_store.chats.add_chats(chats)
        return chats
