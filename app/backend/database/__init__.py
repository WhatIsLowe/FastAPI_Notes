from typing import AsyncGenerator

from .database import async_session

async def get_pg_session() -> AsyncGenerator:
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()