from uuid import UUID
from typing import List, Union
from datetime import datetime

from pydantic import BaseModel, field_validator

from src.schemas.attachment import AttachmentOut


class MessageIn(BaseModel):
    chat_id: Union[UUID, str]
    text: str
    telegram_message_id: int
    is_admin: bool

    @field_validator("text", mode="before")
    @classmethod
    def capitalize(cls, value: str) -> str:
        return value.strip()


class MessageOut(BaseModel):
    id: UUID
    chat_id: UUID
    text: str
    telegram_message_id: int
    is_admin: bool
    created_at: datetime
    updated_at: datetime


class MessageWithAttachmentsIn(MessageIn):
    attachments_ids: List[Union[UUID, str]] = []


class FullMessageOut(MessageOut):
    attachments: List[AttachmentOut] = []
