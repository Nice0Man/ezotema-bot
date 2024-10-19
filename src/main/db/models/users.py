from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from src.main.db.models.base import Base

if TYPE_CHECKING:
    pass


class User(Base):
    id: Mapped[int] = mapped_column(String(255), primary_key=True, nullable=False)
    username: Mapped[str | None] = mapped_column(String(128))
    email: Mapped[str | None] = mapped_column(String(128))
    chat_id: Mapped[int | None]
