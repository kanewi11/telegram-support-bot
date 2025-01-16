import json
from json.decoder import JSONDecodeError
from contextlib import suppress
from typing import List, Any, Dict

from fastapi import WebSocket
from pydantic import BaseModel


class ConnectionService:
    def __init__(self) -> None:
        self.active_connections: Dict[str, List[WebSocket]] = {}

    async def connect(
        self,
        websocket: WebSocket,
        broadcast_id: str
    ) -> None:
        """accept and append the connection to the list"""
        await websocket.accept()
        if self.active_connections.get(broadcast_id):
            self.active_connections[broadcast_id].append(websocket)
        else:
            self.active_connections[broadcast_id] = [websocket]

    def disconnect(self, websocket: WebSocket, broadcast_id: str) -> None:
        """remove the connection from list"""
        if self.active_connections.get(broadcast_id):
            try:
                self.active_connections[broadcast_id].remove(websocket)
            except ValueError:
                pass

    async def send_personal(
        self,
        websocket: WebSocket,
        data: Any
    ) -> None:
        """send personal text"""
        valid_data = self._serialize_data_out(data)
        await websocket.send_text(valid_data)

    async def broadcast(
        self,
        data: Any,
        broadcast_id: str,
    ) -> None:
        """send text to the list of connections"""
        valid_data = self._serialize_data_out(data)
        for connection in self.active_connections.get(broadcast_id, []):
            await connection.send_text(valid_data)

    @staticmethod
    def _serialize_data_out(data: Any) -> str:
        """serialization to str"""
        if isinstance(data, list):
            message_data = []
            for data in data:
                if isinstance(data, BaseModel):
                    message_data.append(data.model_dump_json())
            return json.dumps(message_data)
        elif isinstance(data, BaseModel):
            return data.model_dump_json()
        elif isinstance(data, dict):
            return json.dumps(data)
        return str(data)

    @staticmethod
    def _serialize_data_in(data: Any) -> Any | str:
        """serialization text json to dict or return text"""
        with suppress(JSONDecodeError):
            return json.loads(data)
        return str(data)
