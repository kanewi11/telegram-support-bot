from typing import List, Union
from uuid import UUID

from src.repositories.chat import ChatRepository
from src.repositories.message import MessageRepository
from src.schemas.chat import ChatOut, ChatIn
from src.shared.exceptions import NotFoundException


class ChatService:
    def __init__(
        self,
        message_repo: MessageRepository,
        chat_repo: ChatRepository,
    ) -> None:
        self._message_repo = message_repo
        self._chat_repo = chat_repo

    async def add_chat(self, data: Union[ChatIn, dict]) -> ChatOut:
        if isinstance(data, dict):
            data = ChatIn(**data)
        if exist_chat := await self.get_chat_by_telegram_id(data.telegram_id):
            return exist_chat
        chat = await self._chat_repo.add_chat(data.model_dump())
        return ChatOut(**chat)

    async def read_chat(self, chat_id: Union[UUID, str]) -> ChatOut:
        chat = await self._chat_repo.update_chat(chat_id, {"is_read": True})
        if not chat:
            raise NotFoundException
        return ChatOut(**chat)

    async def get_chat_by_telegram_id(
        self,
        telegram_id: int,
    ) -> Union[ChatOut, None]:
        chat = await self._chat_repo.get_chat_by_telegram_id(telegram_id)
        if chat:
            return ChatOut(**chat)
        return None

    async def get_chats(self) -> List[ChatOut]:
        data = await self._chat_repo.get_all_chats()
        return [ChatOut(**chat) for chat in data]
