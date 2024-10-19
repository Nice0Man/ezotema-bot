from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from src.main.db.models.users import User
from src.main.db.schemas.users import UserRead, UserCreate


# Create
async def create_user(session: AsyncSession, user_data: dict) -> UserRead:
    """Create a new user."""
    new_user = User(**user_data)
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    return new_user


# Read All
async def get_all_users(session: AsyncSession) -> list[UserRead]:
    """Get all users from the database."""
    stmt = select(User)
    result = await session.execute(stmt)
    users = result.scalars().all()
    return list(users)


# Read by ID
async def get_user_by_id(session: AsyncSession, user_id: str) -> UserRead | None:
    """Get a user by ID."""
    return await session.get(User, user_id)


# Update
async def update_user(
    session: AsyncSession, user_id: str, update_data: dict
) -> UserRead | None:
    """Update a user by ID."""
    stmt = (
        update(User)
        .where(User.id == user_id)
        .values(**update_data)
        .execution_options(synchronize_session="fetch")
    )
    await session.execute(stmt)
    await session.commit()
    return await get_user_by_id(session, user_id)


async def add_or_update_user(
    session: AsyncSession, user_id: int, username: str, email: str | None, chat_id: int
):
    user = await session.get(User, user_id)
    if user:
        if email:
            user.email = email
        if username:
            user.username = username
    else:
        new_user = UserCreate(
            id=user_id, username=username, email=email, chat_id=chat_id
        )
        session.add(new_user)
    await session.commit()


# Delete
async def delete_user(session: AsyncSession, user_id: str) -> bool:
    """Delete a user by ID."""
    stmt = delete(User).where(User.id == user_id)
    result = await session.execute(stmt)
    await session.commit()
    return result.rowcount > 0
