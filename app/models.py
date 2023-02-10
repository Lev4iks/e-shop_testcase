import uuid

from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, VARCHAR, INTEGER
from app.database import Base


class User(Base):
    __tablename__ = "user"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(VARCHAR(length=128), nullable=False)


class Brand(Base):
    __tablename__ = "brand"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(VARCHAR(length=128), nullable=False)


class Manufacturer(Base):
    __tablename__ = "manufacturer"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(VARCHAR(length=128), nullable=False)


class Product(Base):
    __tablename__ = "product"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(VARCHAR(length=128), nullable=False)
    brand_id = Column(UUID(), ForeignKey("brand.id"), nullable=False)
    manufacturer_id = Column(UUID(), ForeignKey("manufacturer.id"), nullable=False)
    price = Column((INTEGER()), default=0, nullable=False)


class Cart(Base):
    __tablename__ = "cart"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(), ForeignKey("user.id"), nullable=False)


class Cart_Product(Base):
    __tablename__ = "cart_product"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    cart_id = Column(UUID(), ForeignKey("cart.id"), nullable=False)
    product_id = Column(UUID(), ForeignKey("product.id"), nullable=False)
