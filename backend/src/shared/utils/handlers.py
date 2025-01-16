from typing import Any

from fastapi import WebSocket, WebSocketDisconnect

from src.services.chat import ChatService
from src.services.message import MessageService
from src.services.connection import ConnectionService
from src.schemas.message import MessageWithAttachmentsIn


class WebSocketHandler:
    all_broadcast_id = "all"

    def __init__(
        self,
        chat_service: ChatService,
        message_service: MessageService,
        connection_service: ConnectionService,
    ) -> None:
        self.chat_service = chat_service
        self.message_service = message_service
        self.connection_service = connection_service

    async def handle_list_chats(self, websocket: WebSocket) -> None:
        """send chat list"""
        await self.chat_service.get_chats()
        await self.connection_service.connect(websocket, self.all_broadcast_id)
        try:
            while True:
                await websocket.receive_text()
                await self._send_chat_list(websocket)
        except WebSocketDisconnect:
            self.connection_service.disconnect(
                websocket=websocket,
                broadcast_id=self.all_broadcast_id
            )

    async def handle_chat(self, websocket: WebSocket, chat_id: str) -> None:
        """send chat messages or receive new message"""
        await self.connection_service.connect(websocket, chat_id)
        messages = await self.message_service.get_messages_by_chat_id(chat_id)
        await self.connection_service.send_personal(websocket, messages)
        try:
            while True:
                data_in = await websocket.receive_text()
                valid_data_in = self.connection_service._serialize_data_in(
                    data=data_in
                )
                await self._process_new_message(valid_data_in, chat_id)
        except WebSocketDisconnect:
            self.connection_service.disconnect(websocket, chat_id)

    async def _process_new_message(
        self,
        data: Any,
        chat_id: str,
    ) -> None:
        if not isinstance(data, dict):
            return
        message = MessageWithAttachmentsIn(**data)
        if message.text or message.attachments_ids:
            message = await self.message_service.add_message(data=message)
            await self.chat_service.read_chat(chat_id)
            await self.connection_service.broadcast(message, chat_id)

    async def _send_chat_list(self, websocket: WebSocket) -> None:
        messages = await self.chat_service.get_chats()
        await self.connection_service.send_personal(websocket, messages)
