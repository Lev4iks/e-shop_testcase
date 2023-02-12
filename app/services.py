from typing import Union

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, delete
from sqlalchemy.sql import functions

from app.models import Customer, Product, Cart
from app.schemas import (ShowCustomer, CreateCustomer, FiltersProduct, ShowProduct,
                         CreateProduct, AddRemoveProductFromCart, ShowCart, ProductInCart)


async def create_new_customer(body: CreateCustomer, db_session: AsyncSession) -> ShowCustomer:
    async with db_session.begin():
        new_customer = Customer(name=body.name)
        db_session.add(new_customer)
        await db_session.flush()
        return ShowCustomer(customer_id=new_customer.id, name=new_customer.name)


async def get_customer_by_id(customer_id, db_session: AsyncSession) -> Union[ShowCustomer, None]:
    async with db_session.begin():
        query = select(Customer).where(Customer.id == customer_id)
        res = await db_session.execute(query)
        customer_row = res.fetchone()
        if customer_row is not None:
            customer = customer_row[0]
            return ShowCustomer(customer_id=customer.id, name=customer.name)


async def create_new_product(body: CreateProduct, db_session: AsyncSession) -> ShowProduct:
    async with db_session.begin():
        new_product = Product(name=body.name, brand=body.brand,
                              manufacturer=body.manufacturer, price=body.price)
        db_session.add(new_product)
        await db_session.flush()
        return ShowProduct(product_id=new_product.id, name=new_product.name, brand=new_product.brand,
                           manufacturer=new_product.manufacturer, price=new_product.price)


async def get_products_by_filters(filters: FiltersProduct, db_session: AsyncSession) -> list[ShowProduct]:
    async with db_session.begin():
        if filters.name:
            query = select(Product).filter(
                Product.name.match(filters.name)
            )
            if filters.price:
                query = select(Product).filter(
                    and_(
                        Product.name.match(filters.name),
                        Product.price == filters.price,
                    )
                )
        elif filters.price:
            query = select(Product).filter(
                Product.price == filters.price
            )
        else:
            query = select(Product)

        if filters.order_by == 'name':
            query = query.order_by(Product.name.desc()) if filters.desc else query.order_by(Product.name)
        elif filters.order_by == 'price':
            query = query.order_by(Product.price.desc()) if filters.desc else query.order_by(Product.price)

        res = await db_session.execute(query)
        product_rows = res.fetchall()
        products = [
            ShowProduct(product_id=product_row[0].id, name=product_row[0].name, brand=product_row[0].brand,
                        manufacturer=product_row[0].manufacturer, price=product_row[0].price)
            for product_row in product_rows
        ]
        return products


async def get_product_by_id(product, db_session: AsyncSession) -> Union[ShowProduct, None]:
    async with db_session.begin():
        query = select(Product).where(Product.id == product)
        res = await db_session.execute(query)
        product_row = res.fetchone()
        if product_row is not None:
            product = product_row[0]
            return ShowProduct(product_id=product.id, name=product.name, brand=product.brand,
                               manufacturer=product.manufacturer, price=product.price)


async def get_cart_by_customer_id(customer_id: int, db_session: AsyncSession) -> ShowCart:
    async with db_session.begin():
        query = select(Cart.product_id.distinct(), Product.name,
                       functions.count(Cart.product_id), functions.sum(Product.price)).join(Product).where(
            Cart.customer_id == customer_id).group_by(Cart.product_id, Product.name)
        res = await db_session.execute(query)
        product_in_cart_rows = res.fetchall()
        total_count, total_price = 0, 0
        products = []
        for product_in_cart_row in product_in_cart_rows:
            products.append(
                ProductInCart(product_id=product_in_cart_row[0], name=product_in_cart_row[1],
                              sub_total_count=product_in_cart_row[2], sub_total_price=product_in_cart_row[3])
            )
            total_count += product_in_cart_row[2]
            total_price += product_in_cart_row[3]
        return ShowCart(customer_id=customer_id, products=products, total_count=total_count, total_price=total_price)


async def add_product_into_cart(body: AddRemoveProductFromCart, db_session: AsyncSession) -> ShowCart:
    async with db_session.begin():
        for _ in range(body.count):
            new_item = Cart(customer_id=body.customer_id, product_id=body.product_id)
            db_session.add(new_item)
        await db_session.flush()
    return await get_cart_by_customer_id(body.customer_id, db_session)


async def remove_product_from_cart(body: AddRemoveProductFromCart, db_session: AsyncSession) -> ShowCart:
    async with db_session.begin():
        query = select(
            Cart.id).where(
            Cart.product_id == body.product_id, Cart.customer_id == body.customer_id).limit(body.count)
        res = await db_session.execute(query)
        product_ids_to_delete = [row[0] for row in res.fetchall()]
        if not product_ids_to_delete:
            raise HTTPException(status_code=404, detail=f"Product with id {body.customer_id} not found in the cart.")
        query = delete(Cart).where(Cart.id.in_(product_ids_to_delete))
        await db_session.execute(query)
        await db_session.flush()
    return await get_cart_by_customer_id(body.customer_id, db_session)
