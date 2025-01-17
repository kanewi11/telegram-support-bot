from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart

from src.shared.text import MESSAGES


router = Router()


@router.message(CommandStart())
async def start(
    message: Message,
) -> None:
    await message.answer(MESSAGES.start)
