from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".envs/.env", env_file_encoding="utf-8", extra="ignore"
    )
    # Other
    base_dir: Path = Path(__file__).parent.parent
    messages_file_path: Path = base_dir.parent.joinpath("messages.yml")

    # Bot
    bot_token: str

    # Backend
    backend_host: str
    backend_ssl: bool


@lru_cache
def get_settings() -> Settings:
    return Settings()  # type: ignore


SETTINGS = get_settings()
