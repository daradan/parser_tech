from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, func
from sqlalchemy.orm import relationship

from database import Base, engine


class TechnodomProducts(Base):
    __tablename__ = 'technodom_products'
    id = Column(Integer, primary_key=True, index=True)
    created = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    name = Column(String, nullable=False)
    url = Column(String, nullable=False)
    brand = Column(String, nullable=False)
    category = Column(String, nullable=False)
    color = Column(String)
    images = Column(String, nullable=False)

    prices = relationship('TechnodomPrices', back_populates='product')


class TechnodomPrices(Base):
    __tablename__ = 'technodom_prices'
    id = Column(Integer, primary_key=True, index=True)
    created = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    price = Column(String, nullable=False)
    discount = Column(String)
    product_id = Column(Integer, ForeignKey(TechnodomProducts.id))

    product = relationship('TechnodomProducts', back_populates='prices')


Base.metadata.create_all(engine)
