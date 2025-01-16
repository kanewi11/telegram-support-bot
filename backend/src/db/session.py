from abc import ABC, abstractmethod
from contextlib import asynccontextmanager
from functools import lru_cache
from typing import AsyncIterator
import logging
import traceback

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine
from sqlalchemy.ext.asyncio.session import async_sessionmaker

from src.db.base import async_engine


logger = logging.getLogger(__name__)


class BaseSessionManager(ABC):
    @abstractmethod
    @asynccontextmanager  # type: ignore
    async def manager(self) -> AsyncIterator[AsyncSession]:
        pass


class SessionManager(BaseSessionManager):
    def __init__(self, engine: AsyncEngine = async_engine) -> None:
        self._async_engine = engine
        self._async_session_creator = async_sessionmaker(
            self._async_engine, class_=AsyncSession, expire_on_commit=False
        )

    @asynccontextmanager
    async def manager(self) -> AsyncIterator[AsyncSession]:
        new_session = self._async_session_creator()
        try:
            yield new_session
            await new_session.commit()
        except SQLAlchemyError:
            logger.critical(traceback.format_exc())
            await new_session.rollback()
        finally:
            await new_session.close()


@lru_cache()
def get_session_manager() -> SessionManager:
    return SessionManager()
