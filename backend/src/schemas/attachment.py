from uuid import UUID
from datetime import datetime

from pydantic import BaseModel


class AttachmentIn(BaseModel):
    file_id: str
    mime_type: str


class AttachmentOut(BaseModel):
    id: UUID
    file_id: str
    mime_type: str
    created_at: datetime
    updated_at: datetime


class UploadAttachmentIn(BaseModel):
    ...


class UploadAttachmentOut(BaseModel):
    ...
