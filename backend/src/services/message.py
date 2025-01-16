from typing import Union, List
from uuid import UUID

from src.repositories.message import MessageRepository
from src.repositories.message_attachment import MessageAttachmentRepository
from src.schemas.message import (
    MessageIn,
    MessageOut,
    MessageWithAttachmentsIn,
    FullMessageOut
)
from src.schemas.attachment import AttachmentOut
from src.schemas.message_attachment import MessageAttachmentIn


class MessageService:
    def __init__(
        self,
        repo: MessageRepository,
        message_attachment_repo: MessageAttachmentRepository,
    ) -> None:
        self._repo = repo
        self._message_attachment_repo = message_attachment_repo

    async def get_messages_by_chat_id(
        self,
        chat_id: Union[UUID, str]
    ) -> List[FullMessageOut]:
        data = await self._repo.get_messages_by_chat_id(
            chat_id=chat_id
        )
        messages = []
        for message in data:
            messages.append(self._join_attachments(message))
        return messages

    async def get_message(
        self,
        message_id: Union[UUID, str]
    ) -> FullMessageOut:
        data = await self._repo.get_message_by_id(message_id)
        return self._join_attachments(data)

    async def add_message(
        self,
        data: Union[MessageWithAttachmentsIn, dict]
    ) -> FullMessageOut:
        if isinstance(data, dict):
            data = MessageWithAttachmentsIn(**data)
        message_data = MessageIn(**data.model_dump())
        message = await self._repo.add_message(message_data.model_dump())
        message = FullMessageOut(**message)
        for attachment_id in data.attachments_ids:
            message_attachment_data = MessageAttachmentIn(
                message_id=message.id,
                attachment_id=attachment_id,
            )
            await self._message_attachment_repo.add_message_attachment(
                data=message_attachment_data.model_dump()
            )
        if data.attachments_ids:
            message = await self._repo.get_message_by_id(message.id)
            message = FullMessageOut(**message)
        return message

    @staticmethod
    def _join_attachments(data: dict) -> FullMessageOut:
        attachments = []
        for attachment in data["attachments"]:
            attachments.append(AttachmentOut(**attachment))
        data["attachments"] = attachments
        return FullMessageOut(**data)
