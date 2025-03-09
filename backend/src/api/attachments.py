import imghdr
from pathlib import Path
from uuid import uuid4
from tempfile import NamedTemporaryFile

from fastapi import UploadFile, Depends
from fastapi.responses import FileResponse

from src.core.factories import get_attachment_service
from src.shared.utils.routers import router_factory
from src.shared.utils.image import is_image
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
    with NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(await file.read())
        temp_file_path = temp_file.name  # Путь к временному файлу

    if is_image(temp_file_path):
        file_field = "photo"
    else:
        file_field = "document"
    with open(temp_file_path, "rb") as f:
        response = httpx.post(
            url, 
            data={"chat_id": CHAT_ID}, 
            files={file_field: f}
        )
        return response.json()  # Возвращаем ответ Telegram API
    os.remove(temp_file_path)


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
