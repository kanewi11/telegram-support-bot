from uuid import UUID
from typing import Type, List, Union

from sqlalchemy import select, update, insert

from src.db.models.chat import Chat
from src.repositories.base import BaseCRUDRepository


class ChatRepository(BaseCRUDRepository[Chat]):
    def __init__(self, model: Type[Chat] = Chat) -> None:
        super().__init__(model=model)

    async def get_all_chats(self) -> List[dict]:
        stmt = select(self.model).order_by(self.model.updated_at.desc())
        return await self.get_all(stmt)

    async def update_chat(
        self,
        chat_id: Union[UUID, str],
        data: dict
    ) -> dict:
        stmt = (
            update(self.model)
            .where(self.model.id == chat_id)
            .values(**data)
        )
        return await self.update(stmt)

    async def update_chat_by_telegram_id(
        self,
        telegram_id: int,
        data: dict,
    ) -> dict:
        stmt = (
            update(self.model)
            .where(self.model.telegram_id == telegram_id)
            .values(**data)
        )
        return await self.update(stmt)

    async def get_chat_by_telegram_id(self, telegram_id: int) -> dict:
        stmt = select(self.model).where(self.model.telegram_id == telegram_id)
        return await self.get_one(stmt)

    async def get_chat_by_id(self, profile_id: Union[UUID, str]) -> dict:
        stmt = select(self.model).where(self.model.id == profile_id)
        return await self.get_one(stmt)

    async def add_chat(self, data: dict) -> dict:
        stmt = insert(self.model).values(**data)
        return await self.create_one(stmt)
