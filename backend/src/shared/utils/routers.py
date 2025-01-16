from fastapi import APIRouter

from src.core.config import SETTINGS


def router_factory(
    root_path: str,
) -> APIRouter:
    if SETTINGS.api_url_prefix[-1] == "/":
        raise ValueError(
            "Env var 'API_URL_PREFIX' mustn't end with '/'. For example: '/api_v2'"
        )

    if root_path[0] == "/":
        root_path = root_path[1:]

    return APIRouter(
        prefix=f"{SETTINGS.api_url_prefix}/{root_path}",
    )
