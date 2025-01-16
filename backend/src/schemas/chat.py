from uuid import UUID
from typing import List, Union
from datetime import datetime

from pydantic import BaseModel

from src.schemas.attachment import AttachmentOut
from src.schemas.message import MessageOut


class ChatIn(BaseModel):
    telegram_id: int
    first_name: str
    is_read: bool


class ChatOut(BaseModel):
    id: UUID
    telegram_id: int
    first_name: str
    is_read: bool
    created_at: datetime
    updated_at: datetime
