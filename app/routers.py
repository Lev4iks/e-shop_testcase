from logging import getLogger

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app import services
from app.schemas import ShowCustomer, CreateCustomer, ShowProduct, FiltersProduct, CreateProduct
from app.database import get_db_session

logger = getLogger(__name__)

customer_router = APIRouter()
product_router = APIRouter()


@customer_router.get("/", response_model=ShowCustomer)
async def get_customer_by_id(customer_id: int, db_session: AsyncSession = Depends(get_db_session)) -> ShowCustomer:
    customer = await services.get_customer_by_id(customer_id, db_session)
    if customer is None:
        raise HTTPException(status_code=404, detail=f"Customer with id {customer_id} not found.")
    return customer


@customer_router.post("/", response_model=ShowCustomer)
async def create_customer(body: CreateCustomer, db_session: AsyncSession = Depends(get_db_session)) -> ShowCustomer:
    try:
        return await services.create_new_customer(body, db_session)
    except IntegrityError as err:
        logger.error(err)
        raise HTTPException(status_code=503, detail=f"Database error: {err}")


@product_router.post("/", response_model=ShowProduct)
async def create_product(body: CreateProduct = Depends(CreateProduct),
                         db_session: AsyncSession = Depends(get_db_session)) -> ShowProduct:
    try:
        return await services.create_new_product(body, db_session)
    except IntegrityError as err:
        logger.error(err)
        raise HTTPException(status_code=503, detail=f"Database error: {err}")


@product_router.get("/", response_model=list[ShowProduct])
async def get_products(name: str = None, price: int = None, order_by: str = None, desc: bool = False,
                       db_session: AsyncSession = Depends(get_db_session)) -> list[ShowProduct]:
    filters = FiltersProduct(name=name, price=price, order_by=order_by, desc=desc)
    products = await services.get_products_by_filters(filters, db_session)
    return products


@product_router.get("/{product_id}", response_model=ShowProduct)
async def get_product_by_id(product_id: int,
                            db_session: AsyncSession = Depends(get_db_session)) -> ShowProduct:
    product = await services.get_product_by_id(product_id, db_session)
    if product is None:
        raise HTTPException(status_code=404, detail=f"Product with id {product_id} not found.")
    return product
