from functools import lru_cache, cached_property
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".envs/.env", env_file_encoding="utf-8", extra="ignore"
    )

    # OTHER
    base_dir: Path = Path(__file__).parent.parent
    api_url_prefix: str
    uploads_dir: Path = Path(__file__).parent.parent.joinpath("uploads")
    uploads_dir.mkdir(exist_ok=True)

    # LOCALES
    domain: str = "messages"

    # DATABASE
    postgres_host: str
    postgres_db: str
    postgres_port: str
    postgres_user: str
    postgres_password: str

    @cached_property
    def postgres_dsn(self) -> str:
        postgres_url = (
            f"{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}"
            f"/{self.postgres_db}"
        )
        return f"postgresql+asyncpg://{postgres_url}"


@lru_cache
def get_settings() -> Settings:
    return Settings()  # type: ignore


SETTINGS = get_settings()
