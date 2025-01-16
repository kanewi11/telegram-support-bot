from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.db.models.base import ModelBase


class MessageAttachment(ModelBase):
    __tablename__ = "message_attachment"

    message_id: Mapped[UUID] = mapped_column(
        ForeignKey("message.id"),
        nullable=False,
    )
    attachment_id: Mapped[UUID] = mapped_column(
        ForeignKey("attachment.id"),
        nullable=False,
    )
