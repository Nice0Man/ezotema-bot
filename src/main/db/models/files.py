from typing import TYPE_CHECKING

from src.main.db.models.base import Base
from sqlalchemy import ForeignKey, Integer, LargeBinary, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from src.main.db.models.courses import Course


class File(Base):
    file_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    course_id: Mapped[int] = mapped_column(
        ForeignKey("courses.course_id"), nullable=False
    )
    filename: Mapped[str] = mapped_column(String(255), nullable=False)
    content: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)
    content_type: Mapped[str] = mapped_column(String(50), nullable=False)
    course: Mapped["Course"] = relationship("Course", back_populates="files")
