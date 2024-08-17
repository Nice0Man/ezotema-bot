from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.main.db.models.courses import Course
from src.main.db.schemas.courses import CourseRead


async def get_all(session: AsyncSession):
    """
    Get all courses from the database.
    """
    stmt = select(Course).options(selectinload(Course.files))
    result = await session.execute(stmt)
    courses = result.scalars().all()
    return list(courses)


async def get_by_id(session: AsyncSession, course_id: int) -> CourseRead | None:
    """
    Get a course by ID.
    """
    return await session.get(Course, course_id)


async def get_all_with_files(session: AsyncSession) -> list[CourseRead]:
    """
    Get all courses from the database with associated files.
    """
    stmt = select(Course).options(selectinload(Course.files)).order_by(Course.name)
    result = await session.execute(stmt)
    courses = result.scalars().all()
    return list(courses)


async def get_by_id_with_files(
    session: AsyncSession, course_id: int
) -> CourseRead | None:
    """
    Get a course by ID with associated files.
    """
    stmt = (
        select(Course)
        .options(selectinload(Course.files))
        .where(Course.course_id == course_id)
    )
    result = await session.execute(stmt)
    return result.scalars().one_or_none()
