import re

from fastapi import HTTPException
from pydantic import BaseModel
from pydantic import validator

LETTER_MATCH_PATTERN = re.compile(r"^[а-яА-Яa-zA-Z\-]+$")


class TunedModel(BaseModel):
    class Config:
        orm_mode = True


class ShowCustomer(TunedModel):
    customer_id: int
    name: str


class CreateCustomer(BaseModel):
    name: str

    @validator("name")
    def validate_name(cls, value):
        if not LETTER_MATCH_PATTERN.match(value):
            raise HTTPException(
                status_code=422,
                detail="name should contains only letters"
            )
        return value


class ShowProduct(TunedModel):
    product_id: int
    name: str
    brand: str
    manufacturer: str
    price: int


class CreateProduct(BaseModel):
    name: str
    brand: str
    manufacturer: str
    price: int


class FiltersProduct(BaseModel):
    name: str = None
    price: int = None
    order_by: str = None
    desc: bool = None

    @validator("order_by")
    def validate_order_by(cls, value):
        if value:
            if value.lower() not in ("price", "name"):
                raise HTTPException(
                    status_code=422,
                    detail="order_by should contains only 'price' or 'name'"
                )
            return value.lower()
        return value


class AddRemoveProductFromCart(BaseModel):
    customer_id: int
    product_id: int
    count: int

    @validator("count")
    def validate_count(cls, value):
        if value < 1:
            raise HTTPException(
                status_code=422,
                detail="count can't be less then 1"
            )
        return value


class ProductInCart(TunedModel):
    product_id: int
    name: str
    sub_total_count: int
    sub_total_price: int


class ShowCart(TunedModel):
    customer_id: int
    products: list[ProductInCart]
    total_count: int
    total_price: int
