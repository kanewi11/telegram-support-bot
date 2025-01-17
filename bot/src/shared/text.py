import yaml
from functools import lru_cache

from pydantic import BaseModel

from src.core.config import SETTINGS


class Messages(BaseModel):
    start: str
    wait_reply: str


@lru_cache
def get_messages() -> Messages:
    with open(SETTINGS.messages_file_path, "r", encoding="utf-8") as messages_file:
        messages = yaml.safe_load(messages_file)
    return Messages(**messages)


MESSAGES = get_messages()
