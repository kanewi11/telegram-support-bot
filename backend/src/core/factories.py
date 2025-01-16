from functools import lru_cache

from src.services.chat import ChatService
from src.services.message import MessageService
from src.services.attachment import AttachmentService
from src.services.connection import ConnectionService
from src.repositories.chat import ChatRepository
from src.repositories.message import MessageRepository
from src.repositories.attachment import AttachmentRepository
from src.repositories.message_attachment import MessageAttachmentRepository
from src.shared.utils.handlers import WebSocketHandler


@lru_cache
def get_connection_service() -> ConnectionService:
    return ConnectionService()


@lru_cache
def get_chat_service() -> ChatService:
    return ChatService(
        message_repo=MessageRepository(),
        chat_repo=ChatRepository()
    )


@lru_cache
def get_message_service() -> MessageService:
    return MessageService(
        repo=MessageRepository(),
        message_attachment_repo=MessageAttachmentRepository(),
    )


@lru_cache
def get_attachment_service() -> AttachmentService:
    return AttachmentService(repo=AttachmentRepository())


@lru_cache
def get_websocket_handler() -> WebSocketHandler:
    return WebSocketHandler(
        chat_service=get_chat_service(),
        message_service=get_message_service(),
        connection_service=get_connection_service(),
    )
