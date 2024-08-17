from sqlalchemy import Float, BigInteger, VARCHAR, TEXT
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.main.db.models.base import Base
from src.main.db.models.files import File


class Course(Base):
    course_id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
    )
    name: Mapped[str] = mapped_column(VARCHAR(32))
    description: Mapped[str] = mapped_column(TEXT)
    level: Mapped[int]
    price: Mapped[float] = mapped_column(Float(2))

    # Use string-based relationship definition to prevent circular dependency issues
    files: Mapped[list["File"]] = relationship(
        "File",
        back_populates="course",
        cascade="all, delete-orphan",
    )
