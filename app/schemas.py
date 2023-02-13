import re

from fastapi import HTTPException
from pydantic import BaseModel, validator

LETTER_MATCH_PATTERN = re.compile(r"^[а-яА-Яa-zA-Z\-\s]+$")


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
        if len(value) > 128:
            raise HTTPException(
                status_code=422,
                detail="max length of name is 128 characters"
            )
        if not value.replace(' ', ''):
            raise HTTPException(
                status_code=422,
                detail="name can't be empty"
            )
        return value.strip()


class ShowProduct(TunedModel):
    product_id: int
    name: str
    brand: str
    manufacturer: str
    price: float


class CreateProduct(BaseModel):
    name: str
    brand: str
    manufacturer: str
    price: float

    @validator("name", "brand", "manufacturer")
    def validate_string(cls, value):
        if value:
            if len(value) > 128:
                raise HTTPException(
                    status_code=422,
                    detail="max length of name|brand|manufacturer is 128 characters"
                )
            if not value.replace(' ', ''):
                raise HTTPException(
                    status_code=422,
                    detail="name|brand|manufacturer can't be empty"
                )
        return value.strip()

    @validator("price")
    def validate_price_size(cls, value):
        if value:
            if not 0 <= value <= 2147483647:
                raise HTTPException(
                    status_code=422,
                    detail="ensure this value is greater than or equal to 0 and less than or equal to 2147483647"
                )
        return value


class FiltersProduct(BaseModel):
    name: str = None
    price: float = None
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

    @validator("name")
    def validate_name(cls, value):
        if value:
            if len(value) > 128:
                raise HTTPException(
                    status_code=422,
                    detail="max length of name is 128 characters"
                )
        return value

    @validator("price")
    def validate_int_size(cls, value):
        if value:
            if not 0 <= value <= 2147483647:
                raise HTTPException(
                    status_code=422,
                    detail="ensure this value is greater than or equal to 0 and less than or equal to 2147483647"
                )
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
        if not value <= 2147483647:
            raise HTTPException(
                status_code=422,
                detail="ensure this value is less than or equal to 2147483647"
            )
        return value

    @validator("customer_id", "product_id")
    def validate_ids(cls, value):
        if value:
            if not -2147483648 <= value <= 2147483647:
                raise HTTPException(
                    status_code=422,
                    detail="ensure this value is greater than or equal to -2147483648 "
                           "and less than or equal to 2147483647"
                )
        return value


class ProductInCart(TunedModel):
    product_id: int
    name: str
    sub_total_count: int
    sub_total_price: float


class ShowCart(TunedModel):
    customer_id: int
    products: list[ProductInCart]
    total_count: int
    total_price: float
