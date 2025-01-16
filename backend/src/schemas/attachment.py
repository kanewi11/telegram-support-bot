from uuid import UUID
from datetime import datetime

from pydantic import BaseModel


class AttachmentIn(BaseModel):
    filename: str
    content_type: str


class AttachmentOut(BaseModel):
    id: UUID
    filename: str
    content_type: str
    created_at: datetime
    updated_at: datetime
