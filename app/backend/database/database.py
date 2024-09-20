from envparse import env

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.asyncio.session import async_sessionmaker

env.read_envfile()

engine_pg = create_async_engine(
    "postgresql+asyncpg://{user}:{password}@{host}:{port}/{dbname}".format(
        user=env.str("POSTGRES_USER"),
        password=env.str("POSTGRES_PASSWORD"),
        host=env.str("POSTGRES_HOST"),
        port=env.int("POSTGRES_PORT"),
        dbname=env.str("POSTGRES_DBNAME"),
    ),
    echo=True,
    pool_size=4,
    max_overflow=0,
    pool_recycle=300,
    pool_timeout=120,
)

async_session = async_sessionmaker(
    engine_pg, class_=AsyncSession, expire_on_commit=False, autoflush=False, autocommit=False
)
