import pprint
import random

from src.db.base import async_engine, Base
from src.db.models.chat import Chat
from src.db.models.message import Message
from src.db.models.attachment import Attachment
from src.db.models.message_attachment import MessageAttachment
from src.schemas.attachment import AttachmentIn
from src.schemas.chat import ChatIn
from src.schemas.message import MessageWithAttachmentsIn
from src.core.factories import (
    get_attachment_service,
    get_chat_service,
    get_message_service
)


async def start() -> None:
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    for _ in range(100):
        chat_data = ChatIn(
            telegram_id=random.randint(10000, 200000),
            first_name="bond",
            is_read=False,
        )
        chat_service = get_chat_service()
        chat = await chat_service.add_chat(chat_data)
    
    attachment_data = AttachmentIn(
        content_type="text/html",
        filename="hello.png",
    )
    attachment_service = get_attachment_service()
    attachment1 = await attachment_service.add_attachment(attachment_data)
    attachment2 = await attachment_service.add_attachment(attachment_data)

    message_data = MessageWithAttachmentsIn(
        chat_id=chat.id,
        text="hello",
        telegram_message_id=1,
        is_admin=False,
        attachments_ids=[attachment1.id, attachment2.id],
    )
    message_data_2 = MessageWithAttachmentsIn(
        chat_id=chat.id,
        text="hi!",
        telegram_message_id=2,
        is_admin=True
    )
    message_service = get_message_service()
    await message_service.add_message(message_data)
    await message_service.add_message(message_data_2)
    
    # chats = await chat_service.get_chats()
    # for chat in chats:
    #     pprint.pp(chat.model_dump_json())
    chat_messages = await message_service.get_messages_by_chat_id(chat.id)
    for chat_message in chat_messages:
        pprint.pp(chat_message.model_dump_json())
