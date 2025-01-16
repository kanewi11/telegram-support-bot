from sqlalchemy import String, BigInteger, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.models.base import ModelBase
from src.db.models.message import Message


class Chat(ModelBase):
    __tablename__ = "chat"

    telegram_id: Mapped[int] = mapped_column(
        BigInteger(), nullable=False, unique=True
    )
    first_name: Mapped[str] = mapped_column(String(300), nullable=False)
    is_read: Mapped[bool] = mapped_column(Boolean(), nullable=False)
