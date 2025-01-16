from uuid import UUID
from typing import Union

from pydantic import BaseModel


class MessageAttachmentIn(BaseModel):
    message_id: Union[UUID, str]
    attachment_id: Union[UUID, str]
