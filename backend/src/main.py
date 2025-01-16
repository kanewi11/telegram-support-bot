from typing import Any, Dict

from fastapi import FastAPI
from fastapi.routing import APIRoute
from fastapi.openapi.utils import get_openapi
from fastapi.middleware.cors import CORSMiddleware

from src.api.attachments import router as attachment_router
from src.api.chats import router as chat_router
from src.core.config import SETTINGS


app = FastAPI(debug=True)

for router in (
    attachment_router,
    chat_router,
):
    app.include_router(router)


def use_controller_method_names_as_operation_ids(app: FastAPI) -> None:
    """
    Позволяет генерировать operationId на основе __name__ методов контроллеров

    Все методы должны иметь уникальные имена
    """
    for route in app.routes:
        if isinstance(route, APIRoute):
            route.operation_id = route.endpoint.__name__


def custom_openapi() -> Dict[str, Any]:
    # Кэширование
    if app.openapi_schema:
        return app.openapi_schema
    # Кастомизация
    openapi_schema = get_openapi(
        title="Telegram SRM",
        version="0.1b",
        routes=app.routes,
    )
    openapi_schema["paths"][f"{SETTINGS.api_url_prefix}/chats/ws"] = {
        "get": {
            "summary": "Получение чатов через Websocket",
            "description": "Получить все чаты с последним сообщением в нем и помечать их прочитанными",
            "responses": {
                "200": {"description": "WebSocket"},
                "101": {
                    "description": "Switching Protocols - The client is switching protocols as requested by the server.",
                }
            }
        }
    }
    openapi_schema["paths"][f"{SETTINGS.api_url_prefix}/chats/ws/" + "{chat_id}"] = {
        "get": {
            "summary": "Получение и отправка сообщений через Websocket",
            "description": "Получить все сообщения при подключении и отправить новое сообщение",
            "responses": {
                "200": {"description": "WebSocket"},
                "101": {
                    "description": "Switching Protocols - The client is switching protocols as requested by the server.",
                }
            }
        }
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
