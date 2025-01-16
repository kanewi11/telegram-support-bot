from fastapi import Depends, WebSocket, WebSocketDisconnect

from src.core.factories import (
    get_chat_service,
    get_message_service,
    get_connection_service,
    get_websocket_handler,
)
from src.schemas.chat import ChatIn, ChatOut
from src.services.chat import ChatService
from src.services.message import MessageService
from src.services.connection import ConnectionService
from src.shared.utils.routers import router_factory
from src.shared.utils.handlers import WebSocketHandler
from src.schemas.message import MessageWithAttachmentsIn


router = router_factory("chats")


@router.post(
    "/",
    name="Создать чат",
    response_model=ChatOut,
)
async def create_chat(
    new: ChatIn,
    service: ChatService = Depends(get_chat_service),
) -> ChatOut:
    return await service.add_chat(new)


@router.websocket(
    "/ws",
    name="Получить все чаты с последним сообщением",
)
async def list_chats(
    websocket: WebSocket,
    handler: WebSocketHandler = Depends(get_websocket_handler),
) -> None:
    await handler.handle_list_chats(websocket)


@router.websocket(
    "/ws/{chat_id}",
    name="Чат с пользователем",
)
async def chat(
    websocket: WebSocket,
    chat_id: str,
    handler: WebSocketHandler = Depends(get_websocket_handler),
) -> None:
    await handler.handle_chat(websocket, chat_id)
