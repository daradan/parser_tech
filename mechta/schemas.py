from pydantic import BaseModel
from typing import Optional


class ProductSchema(BaseModel):
    name: str
    url: str
    store_id: str
    brand: str = None
    category: str
    images: str


class PriceSchema(BaseModel):
    price: int
    product_id: Optional[int]
    discount: str = '0'
