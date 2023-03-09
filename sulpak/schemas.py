from pydantic import BaseModel
from typing import Optional


class ProductSchema(BaseModel):
    name: str
    url: str
    store_id: int
    brand: str = ''
    category: str
    characteristics: str = ''
    images: str


class PriceSchema(BaseModel):
    price: int
    product_id: Optional[int]
    discount: str = '0'
