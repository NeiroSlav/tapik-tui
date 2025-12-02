from datetime import datetime
from enum import StrEnum
from typing import Annotated, Literal, Union
from uuid import UUID

from pydantic import Field

from core.entities.base import BaseEntity


class InfoActionType(StrEnum):
    GROUP_CREATION = "group_creation"
    THREAD_CREATION = "thread_creation"

    MEMBERS_ADDING = "members_adding"
    MEMBERS_REMOVING = "members_removing"

    OWNER_CHANGING = "owner_changing"
    TYPE_CHANGING = "type_changing"
    NAME_CHANGING = "name_changing"


class InfoContent(BaseEntity):
    type: Literal["info"] = "info"
    action_type: InfoActionType
    actor_id: UUID
    member_ids: set[UUID] | None
    thread_name: str | None = None
    chat_name: str | None = None


class TextContent(BaseEntity):
    type: Literal["text"] = "text"
    text: str


Content = Annotated[Union[InfoContent, TextContent], Field(discriminator="type")]


class Message(BaseEntity):
    user_id: UUID
    chat_id: UUID
    local_id: int
    content: Content
    created_at: datetime
