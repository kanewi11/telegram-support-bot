from typing import Type

from sqlalchemy import insert

from src.db.models.message_attachment import MessageAttachment
from src.repositories.base import BaseCRUDRepository


class MessageAttachmentRepository(BaseCRUDRepository[MessageAttachment]):
    def __init__(
        self,
        model: Type[MessageAttachment] = MessageAttachment
    ) -> None:
        super().__init__(model=model)

    async def add_message_attachment(self, data: dict) -> dict:
        stmt = insert(self.model).values(**data)
        return await self.create_one(stmt)
