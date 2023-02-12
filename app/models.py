from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import VARCHAR, INTEGER
from app.database import Base


class Customer(Base):
    __tablename__ = "customer"

    id = Column(INTEGER(), primary_key=True)
    name = Column(VARCHAR(length=128), nullable=False)


class Product(Base):
    __tablename__ = "product"

    id = Column(INTEGER(), primary_key=True)
    name = Column(VARCHAR(length=128), nullable=False)
    brand = Column(VARCHAR(length=128), nullable=False)
    manufacturer = Column(VARCHAR(length=128), nullable=False)
    price = Column((INTEGER()), default=0, nullable=False)


class Cart(Base):
    __tablename__ = "cart"

    id = Column(INTEGER(), primary_key=True, index=True)
    customer_id = Column(INTEGER(), ForeignKey("customer.id"), nullable=False)
    product_id = Column(INTEGER(), ForeignKey("product.id"), nullable=False)
