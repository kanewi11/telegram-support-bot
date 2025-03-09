from typing import Union
from uuid import UUID
from string import Template
from tempfile import NamedTemporaryFile

import httpx
from httpx import HTTPError, Response
from fastapi import UploadFile

from src.repositories.attachment import AttachmentRepository
from src.schemas.attachment import AttachmentIn, AttachmentOut
from src.shared.exceptions import (
    NotFoundException,
    FailedFetchError,
    FailedResponseError
)
from src.shared.utils.image import is_image


class AttachmentService:
    _error_message: Template = Template(
        "$status_code\nRequest: $request\nResponse: $response"
    )
    _url_telegram: Template = Template(
        "https://api.telegram.org/bot$bot_token/$endpoint"
    )

    def __init__(
        self,
        bot_token: str,
        repo: AttachmentRepository,
    ) -> None:
        self._bot_token = bot_token
        self._repo = repo

    async def upload_file(self, file: UploadFile, telegram_chat_id: int):
        with NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(await file.read())
            temp_file_path = temp_file.name  # Путь к временному файлу

        if is_image(temp_file_path):
            file_field = "photo"
            endpoint = "sendPhoto"
        else:
            file_field = "document"
            endpoint = "sendDocument"
        url = self._url_telegram.substitute(
            bot_token=self._bot_token,
            endpoint=endpoint
        )
        with open(temp_file_path, "rb") as temp_file:
            request_params = {
                "url": url,
                "data": {
                    "chat_id": telegram_chat_id,
                },
                "files": {
                    file_field: temp_file
                }
            }
            telegram_file = await self._make_safe_request(
                http_method="post", 
                request_params=request_params
            )

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

    async def _make_safe_request(
        self, http_method: str, request_params: dict
    ) -> dict:
        """Запрос с обработкой ошибок"""
        try:
            async with httpx.AsyncClient(verify=False) as client:
                method = getattr(client, http_method)
                response: Response = await method(**request_params)
        except HTTPError:
            raise FailedFetchError(request_params.get("url"))

        try:
            response.raise_for_status()
        except HTTPError:
            raise FailedResponseError(
                status_code=response.status_code,
                detail=self._error_message.substitute(
                    status_code=response.status_code,
                    request=request_params,
                    response=response.text,
                )
            )
        return response.json()
