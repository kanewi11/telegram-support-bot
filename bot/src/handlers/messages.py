from aiogram import Router
from aiogram.types import Message

from src.shared.text import MESSAGES


router = Router()


@router.message()
async def message_handler(
    message: Message,
) -> None:
    attachments = []
    if message.document:
        attachments.append(("document", message.document))
    if message.photo:
        attachments.append(("photo", message.photo[-1]))  # Берём последнее фото (наивысшее качество)
    if message.video:
        attachments.append(("video", message.video))
    if message.audio:
        attachments.append(("audio", message.audio))
    if message.voice:
        attachments.append(("voice", message.voice))
    if message.sticker:
        attachments.append(("sticker", message.sticker))
    if message.animation:
        attachments.append(("animation", message.animation))

    response = "Получены вложения:\n"
    for attachment_type, attachment in attachments:
        response += f"- {attachment_type}: {attachment.file_id}\n"
    
    await message.reply(response)
