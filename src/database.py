from typing import AsyncGenerator

from aioredis import Redis, from_url
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeMeta, declarative_base

from src.config import (
    DB_HOST,
    DB_NAME,
    DB_PASS,
    DB_PORT,
    DB_USER,
    RABBITMQ_HOST,
    RABBITMQ_PASSWORD,
    RABBITMQ_PORT,
    RABBITMQ_USERNAME,
    REDIS_HOST,
    REDIS_PORT,
)

DATABASE_URL: str = f'postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
REDIS_URL: str = f'redis://{REDIS_HOST}:{REDIS_PORT}'
RABBITMQ_URL: str = f'amqp://{RABBITMQ_USERNAME}:{RABBITMQ_PASSWORD}@{RABBITMQ_HOST}:{RABBITMQ_PORT}'

Base: DeclarativeMeta = declarative_base()

engine: AsyncEngine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False
)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
        await session.close()


async def get_async_session_() -> AsyncSession:
    async with async_session_maker() as session:
        return session


async def get_redis() -> Redis:
    async with await from_url(REDIS_URL) as redis:
        yield redis
