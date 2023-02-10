from typing import Generator

from fastapi import Depends
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base

from app.config import settings

POSTGRES_URL = f"postgresql+asyncpg://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}" \
               f"@{settings.POSTGRES_HOST}:{settings.DATABASE_PORT}/{settings.POSTGRES_DB}"

engine = create_async_engine(
    POSTGRES_URL,
    future=True,
    echo=True,
)
Base = declarative_base()
async_session = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def get_db_session() -> Generator:
    try:
        session: AsyncSession = async_session()
        yield session
    finally:
        await session.close()


async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Initialized database models")


async def insert_start_data():
    db_session: AsyncSession = Depends(get_db_session)
    async with db_session.begin():
        ...
    logger.info("Initialized database start data")

