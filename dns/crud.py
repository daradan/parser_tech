from typing import Union
from sqlalchemy.orm import Session
from .models import DnsProducts, DnsPrices
# from .database import SessionLocal
from .schemas import ProductSchema, PriceSchema
from . import config

import sys
import os
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
import global_config


class Crud:
    def __init__(self, session: Session, schema):
        self.session = session
        self.schema = schema

    def get(self, pk):
        return self.session.get(self.schema, pk)

    def update(self, data):
        self.session.query(self.schema).filter_by(id=data['id']).update(**data)

    def delete(self, pk):
        self.session.query(self.schema).filter_by(id=pk).delete()

    def insert(self, data: Union[ProductSchema, PriceSchema]):
        obj = self.schema(**data.dict())
        self.session.add(obj)
        self.session.commit()
        return obj


class ProductsCrud(Crud):
    def __init__(self, session: Session, schema):
        super().__init__(session, schema)

    def get_by_url(self, url):
        return self.session.query(self.schema).filter_by(url=url).first()

    def get_or_create(self, new_product: ProductSchema):
        obj = self.get_by_url(new_product.url)
        if obj:
            return obj
        return self.insert(new_product)


class PricesCrud(Crud):
    def __init__(self, session: Session, schema):
        super().__init__(session, schema)

    def get_by_product(self, product_id: int):
        return self.session.query(self.schema).filter_by(product_id=product_id).all()

    def get_last_price(self, product_id: int):
        return self.session.query(self.schema).filter_by(product_id=product_id).order_by(self.schema.created.desc()).\
            first()

    def get_all_prices(self, product_id: int):
        return self.session.query(self.schema).filter_by(product_id=product_id).\
            order_by(self.schema.created.desc()).all()
        # return self.session.query(self.schema).filter_by(product_id=product_id).order_by(self.schema.created.desc()).\
        #     limit(global_config.LAST_N_PRICES).all()


class DnsProductsCrud(ProductsCrud):
    def __init__(self, session: Session):
        super().__init__(session, DnsProducts)


class DnsPricesCrud(PricesCrud):
    def __init__(self, session: Session):
        super().__init__(session, DnsPrices)
