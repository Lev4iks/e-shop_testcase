import json
from typing import Generator

from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from app.config import settings
from app.models import Product, Customer, Base

POSTGRES_URL = f"postgresql+asyncpg://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}" \
               f"@{settings.POSTGRES_HOST}:{settings.DATABASE_PORT}/{settings.POSTGRES_DB}"

engine = create_async_engine(
    POSTGRES_URL
)
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


async def init_start_data():
    with open("start_data.json", "r") as read_file:
        start_data: dict = json.load(read_file)
    products = [
        Product(name=product['name'], brand=product['brand'],
                manufacturer=product['manufacturer'], price=product['price'])
        for product in start_data.get('products')
    ]
    customers = [
        Customer(id=customer['customer_id'], name=customer['name'])
        for customer in start_data.get('customers')
    ]
    db_session = async_session()
    async with db_session.begin():
        db_session.add_all(products)
        db_session.add_all(customers)
    await db_session.flush()
    await db_session.close()
    logger.info("Initialized database start data")
