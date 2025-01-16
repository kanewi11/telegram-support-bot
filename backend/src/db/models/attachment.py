from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.models.base import ModelBase


class Attachment(ModelBase):
    __tablename__ = "attachment"

    content_type: Mapped[str] = mapped_column(String(200), nullable=False)
    filename: Mapped[str] = mapped_column(String(255), nullable=False)
    message: Mapped["Message"] = relationship(  # type: ignore
        "Message",
        secondary="message_attachment",
        back_populates="attachments",
    )
