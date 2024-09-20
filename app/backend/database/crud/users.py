from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models import User
from ...api.schemas.users import UserCreateSchema


async def get_user_by_id(db: AsyncSession, user_id: int) -> Optional[User]:
    res = await db.execute(select(User).where(User.id == user_id))
    return res.scalars().first()


async def get_user_by_username(db: AsyncSession, username: str) -> Optional[User]:
    res = await db.execute(select(User).where(User.username == username))
    return res.scalars().first()


async def get_user_by_phone(db: AsyncSession, phone: str) -> Optional[User]:
    res = await db.execute(select(User).where(User.phone_number == phone))
    return res.scalars().first()


async def create_user(db: AsyncSession, user: UserCreateSchema) -> User:
    if not user.username.strip() or not user.phone_number.strip():
        raise ValueError('Username and phone number is required')

    db_user = User(username=user.username, hashed_password=user.hashed_password, phone_number=user.phone_number)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user
