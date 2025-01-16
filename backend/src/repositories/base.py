from typing import Type, TypeVar, Generic, Any, List, Protocol

from sqlalchemy import Select, Update, Delete, Insert
from sqlalchemy.orm import MappedClassProtocol

from src.db.session import BaseSessionManager, get_session_manager
from src.db.models.base import ModelBase


T = TypeVar("T", bound=ModelBase)


class BaseRepository(Generic[T]):
    def __init__(
        self,
        model: Type[T],
        session: BaseSessionManager = get_session_manager(),
    ) -> None:
        self._model = model
        self._session = session

    @property
    def session(self) -> BaseSessionManager:
        # Read only
        return self._session

    @property
    def model(self) -> Type[T]:
        # Read only
        return self._model


class CRUDRepositoryProtocol(Protocol):
    @property
    def session(self) -> BaseSessionManager: ...

    @property
    def model(self) -> Type[Any]: ...


class ReadRepositoryMixin(CRUDRepositoryProtocol):
    """
    Обработка SELECT запрсов
    """

    async def get_one(self, stmt: Select) -> dict:
        async with self.session.manager() as session:
            result: MappedClassProtocol = (
                await session.execute(stmt)
            ).scalar_one_or_none()
            return result.__dict__ if result else {}

    async def get_all(self, stmt: Select) -> List[dict]:
        async with self.session.manager() as session:
            results = (await session.execute(stmt)).scalars().all()
            return [result.__dict__ for result in results]


class CreateRepositoryMixin(ReadRepositoryMixin, CRUDRepositoryProtocol):
    """
    Обработка INSERT запрсов
    """

    async def bulk_create(self, stmts: List[Insert]) -> List[dict]:
        results = []
        async with self.session.manager() as session:
            for stmt in stmts:
                stmt = stmt.returning(self.model)
                result = (await session.execute(stmt)).scalar_one_or_none()
                results.append(result.__dict__ if result else {})
            return results

    async def create_one(self, stmt: Insert) -> dict:
        stmt = stmt.returning(self.model)
        async with self.session.manager() as session:
            result = (await session.execute(stmt)).scalar_one_or_none()
            return result.__dict__ if result else {}


class UpdateRepositoryMixin(ReadRepositoryMixin, CRUDRepositoryProtocol):
    """
    Обработка UPDATE запрсов
    """

    async def update(self, stmt: Update) -> dict:
        stmt = stmt.returning(self.model)
        async with self.session.manager() as session:
            result = (await session.execute(stmt)).scalar_one_or_none()
            return result.__dict__ if result else {}


class DeleteRepositoryMixin(ReadRepositoryMixin, CRUDRepositoryProtocol):
    """
    Обработка DELETE запрсов
    """

    async def delete(self, stmt: Delete):
        async with self.session.manager() as session:
            await session.execute(stmt)


class BaseCRUDRepository(
    BaseRepository[T],
    CreateRepositoryMixin,
    UpdateRepositoryMixin,
    DeleteRepositoryMixin,
):
    pass
