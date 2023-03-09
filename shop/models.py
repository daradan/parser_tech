from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, func
from sqlalchemy.orm import relationship

from database import Base, engine


class ShopProducts(Base):
    __tablename__ = 'shop_products'
    id = Column(Integer, primary_key=True, index=True)
    created = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    name = Column(String, nullable=False)
    url = Column(String, nullable=False)
    store_id = Column(String, nullable=False)
    brand = Column(String)
    category = Column(String, nullable=False)
    characteristics = Column(String)
    images = Column(String, nullable=False)

    prices = relationship('ShopPrices', back_populates='product')


class ShopPrices(Base):
    __tablename__ = 'shop_prices'
    id = Column(Integer, primary_key=True, index=True)
    created = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    price = Column(String, nullable=False)
    discount = Column(String)
    product_id = Column(Integer, ForeignKey(ShopProducts.id))

    product = relationship('ShopProducts', back_populates='prices')


Base.metadata.create_all(engine)
