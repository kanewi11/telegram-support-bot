from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile, Depends
from fastapi.responses import FileResponse

from src.core.factories import get_attachment_service
from src.shared.utils.routers import router_factory
from src.schemas.attachment import AttachmentIn, AttachmentOut
from src.services.attachment import AttachmentService
from src.core.config import SETTINGS


router = router_factory("attachment")


@router.post(
    "/file",
    response_model=AttachmentOut,
    name="Загрузить вложение на сервер"
)
async def upload_file(
    file: UploadFile,
    service: AttachmentService = Depends(get_attachment_service),
) -> AttachmentOut:
    if file.filename:
        file_prefix = file.filename.split('.')
        if len(file_prefix) > 1:
            file_prefix = f".{file_prefix[-1]}"
    else:
        file_prefix = ""
    file.filename = f"{uuid4().hex}{file_prefix}"
    file_path = SETTINGS.uploads_dir.joinpath(file.filename)
    with open(file_path, "wb") as uploaded_file:
        uploaded_file.write(file.file.read())
    attachment = await service.add_attachment(
        AttachmentIn(
            filename=file.filename,
            content_type=file.content_type or "text/html"
        )
    )
    return attachment


@router.get(
    "/file/{attachment_id}",
    response_class=FileResponse,
    name="Получить вложение",
)
async def get_file(
    attachment_id: str,
    service: AttachmentService = Depends(get_attachment_service),
) -> Path:
    attachment = await service.get_attachment(attachment_id)
    file_path = SETTINGS.uploads_dir.joinpath(attachment.filename)
    return file_path
