from uuid import UUID
from typing import Type, List, Union

from sqlalchemy import select, insert
from sqlalchemy.orm import selectinload

from src.db.models.message import Message
from src.db.models.chat import Chat
from src.db.models.message_attachment import MessageAttachment
from src.db.models.attachment import Attachment
from src.repositories.base import BaseCRUDRepository


class MessageRepository(BaseCRUDRepository[Message]):
    def __init__(self, model: Type[Message] = Message) -> None:
        super().__init__(model=model)

    async def get_message_by_id(self, message_id: Union[UUID, str]) -> dict:
        stmt = (
            select(self.model)
            .where(self.model.id == message_id)
            .options(selectinload(self.model.attachments))
        )
        result = await self.get_one(stmt)
        attachments = []
        for attachment in result["attachments"]:
            attachments.append(attachment.__dict__)
        result["attachments"] = attachments
        return result

    async def get_messages_by_chat_id(
        self,
        chat_id: Union[UUID, str]
    ) -> List[dict]:
        stmt = (
            select(self.model)
            .where(self.model.chat_id == chat_id)
            .order_by(self.model.created_at.asc())
            .options(selectinload(self.model.attachments))
        )
        results = await self.get_all(stmt)
        for result in results:
            attachments = []
            for attachment in result["attachments"]:
                attachments.append(attachment.__dict__)
            result["attachments"] = attachments
        return results

    async def add_message(self, data: dict) -> dict:
        stmt = insert(self.model).values(**data)
        return await self.create_one(stmt)
