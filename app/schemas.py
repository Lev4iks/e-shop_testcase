import re

from typing import Union

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
                detail="Name should contains only letters"
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
    name: Union[str, None] = None
    price: Union[int, None] = None
    order_by: Union[str, None] = None
    desc: Union[bool, None] = None

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
