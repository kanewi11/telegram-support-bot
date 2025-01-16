from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine

from src.core.config import SETTINGS


async_engine = create_async_engine(SETTINGS.postgres_dsn, echo=False)
Base = declarative_base()
