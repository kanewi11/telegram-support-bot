from uuid import UUID
from typing import List

from sqlalchemy import ForeignKey, String, BigInteger, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.models.base import ModelBase
from src.db.models.attachment import Attachment


class Message(ModelBase):
    __tablename__ = "message"

    chat_id: Mapped[UUID] = mapped_column(
        ForeignKey("chat.id"),
        nullable=False,
    )
    text: Mapped[str] = mapped_column(String(4096), nullable=True)
    telegram_message_id: Mapped[int] = mapped_column(BigInteger())
    is_admin: Mapped[bool] = mapped_column(Boolean())

    attachments: Mapped[List[Attachment]] = relationship(
        "Attachment",
        secondary="message_attachment",
        back_populates="message",
    )
