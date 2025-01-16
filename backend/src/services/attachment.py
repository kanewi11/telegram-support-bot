from typing import Union
from uuid import UUID

from src.repositories.attachment import AttachmentRepository
from src.schemas.attachment import AttachmentIn, AttachmentOut
from src.shared.exceptions import NotFoundException


class AttachmentService:
    def __init__(
        self,
        repo: AttachmentRepository,
    ) -> None:
        self._repo = repo

    async def add_attachment(
        self,
        data: Union[AttachmentIn, dict]
    ) -> AttachmentOut:
        if isinstance(data, dict):
            data = AttachmentIn(**data)
        attachment = await self._repo.add_attachment(data.model_dump())
        return AttachmentOut(**attachment)

    async def get_attachment(
        self,
        attachment_id: Union[UUID, str]
    ) -> AttachmentOut:
        attachment_data = await self._repo.get_attachment_by_id(attachment_id)
        if not attachment_data:
            raise NotFoundException
        return AttachmentOut(**attachment_data)
