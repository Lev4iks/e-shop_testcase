from fastapi import APIRouter, HTTPException, Depends, Query, Path
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from loguru import logger

from app import services
from app.schemas import (ShowCustomer, CreateCustomer, ShowProduct,
                         FiltersProduct, CreateProduct, ShowCart, AddRemoveProductFromCart)
from app.database import get_db_session

customer_router = APIRouter()
product_router = APIRouter()
cart_router = APIRouter()


@customer_router.get("/", response_model=ShowCustomer)
async def get_customer_by_id(customer_id: int = Query(ge=-2147483648, le=2147483647),
                             db_session: AsyncSession = Depends(get_db_session)) -> ShowCustomer:
    try:
        customer = await services.get_customer_by_id(customer_id, db_session)
    except Exception as err:
        logger.error(err)
        raise HTTPException(status_code=422,
                            detail=f"id {customer_id} is not acceptable.")
    if not customer:
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
async def create_product(body: CreateProduct,
                         db_session: AsyncSession = Depends(get_db_session)) -> ShowProduct:
    try:
        return await services.create_new_product(body, db_session)
    except IntegrityError as err:
        logger.error(err)
        raise HTTPException(status_code=503, detail=f"Database error: {err}")


@product_router.get("/{product_id}", response_model=ShowProduct)
async def get_product_by_id(product_id: int = Path(ge=-2147483648, le=2147483647),
                            db_session: AsyncSession = Depends(get_db_session)) -> ShowProduct:
    product = await services.get_product_by_id(product_id, db_session)
    if product is None:
        raise HTTPException(status_code=404, detail=f"Product with id {product_id} not found.")
    return product


@product_router.get("/", response_model=list[ShowProduct])
async def get_products(name: str = None, price: float = Query(default=None, ge=-2147483648, le=2147483647),
                       order_by: str = None, desc: bool = False,
                       db_session: AsyncSession = Depends(get_db_session)) -> list[ShowProduct]:
    filters = FiltersProduct(name=name, price=price, order_by=order_by, desc=desc)
    products = await services.get_products_by_filters(filters, db_session)
    return products


@cart_router.get("/", response_model=ShowCart)
async def get_cart_by_customer_id(customer_id: int = Query(ge=-2147483648, le=2147483647),
                                  db_session: AsyncSession = Depends(get_db_session)) -> ShowCart:
    if not await services.get_customer_by_id(customer_id, db_session):
        raise HTTPException(status_code=404, detail=f"Customer with id {customer_id} not found.")
    cart = await services.get_cart_by_customer_id(customer_id, db_session)
    return cart


@cart_router.post("/", response_model=ShowCart)
async def add_product_into_cart(body: AddRemoveProductFromCart,
                                db_session: AsyncSession = Depends(get_db_session)) -> ShowCart:
    if not await services.get_customer_by_id(body.customer_id, db_session):
        raise HTTPException(status_code=404, detail=f"Customer with id {body.customer_id} not found.")
    if not await services.get_product_by_id(body.product_id, db_session):
        raise HTTPException(status_code=404, detail=f"Product with id {body.product_id} not found.")
    try:
        return await services.add_product_into_cart(body, db_session)
    except IntegrityError as err:
        logger.error(err)
        raise HTTPException(status_code=503, detail=f"Database error: {err}")


@cart_router.delete("/", response_model=ShowCart)
async def remove_product_from_cart(body: AddRemoveProductFromCart,
                                   db_session: AsyncSession = Depends(get_db_session)) -> ShowCart:
    if not await services.get_customer_by_id(body.customer_id, db_session):
        raise HTTPException(status_code=404, detail=f"Customer with id {body.customer_id} not found.")
    if not await services.get_product_by_id(body.product_id, db_session):
        raise HTTPException(status_code=404, detail=f"Product with id {body.product_id} not found.")
    try:
        return await services.remove_product_from_cart(body, db_session)
    except IntegrityError as err:
        logger.error(err)
        raise HTTPException(status_code=503, detail=f"Database error: {err}")
