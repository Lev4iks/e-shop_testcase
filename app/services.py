from typing import Union

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_

from app.models import Customer, Product
from app.schemas import ShowCustomer, CreateCustomer, FiltersProduct, ShowProduct, CreateProduct


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
            return ShowCustomer(user_id=customer.id, name=customer.name)


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
