from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.methods import DeleteWebhook
from aiogram.client.default import DefaultBotProperties
from aiogram.utils.callback_answer import CallbackAnswerMiddleware

from src.core.config import SETTINGS
from src.handlers import routers


async def start() -> None:
    dispatcher = Dispatcher()

    # Middlewares
    dispatcher.callback_query.middleware(CallbackAnswerMiddleware())

    # Routes
    dispatcher.include_routers(*routers)

    # Bot
    bot = Bot(
        token=SETTINGS.bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )

    await bot(DeleteWebhook(drop_pending_updates=True))
    await dispatcher.start_polling(bot)
