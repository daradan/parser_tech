from pydantic import BaseModel
from typing import Optional


class ProductSchema(BaseModel):
    name: str
    url: str
    brand: str
    category: str
    color: Optional[str]
    images: str


class PriceSchema(BaseModel):
    price: int
    product_id: Optional[int]
    discount: str = None
    # discount: str
