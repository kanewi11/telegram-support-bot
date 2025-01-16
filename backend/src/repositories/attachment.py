from typing import Type, Union
from uuid import UUID

from sqlalchemy import insert, select

from src.db.models.attachment import Attachment
from src.repositories.base import BaseCRUDRepository


class AttachmentRepository(BaseCRUDRepository[Attachment]):
    def __init__(self, model: Type[Attachment] = Attachment) -> None:
        super().__init__(model=model)
    
    async def get_attachment_by_id(
        self, 
        attachment_id: Union[UUID, str]
    ) -> dict:
        stmt = select(self.model).where(self.model.id == attachment_id)
        return await self.get_one(stmt)
        

    async def add_attachment(self, data: dict) -> dict:
        stmt = insert(self.model).values(**data)
        return await self.create_one(stmt)
