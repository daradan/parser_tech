from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, func
from sqlalchemy.orm import relationship

from database import Base, engine


class MechtaProducts(Base):
    __tablename__ = 'mechta_products'
    id = Column(Integer, primary_key=True, index=True)
    created = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    name = Column(String, nullable=False)
    url = Column(String, nullable=False)
    store_id = Column(String, nullable=False)
    brand = Column(String, nullable=False)
    category = Column(String, nullable=False)
    images = Column(String, nullable=False)

    prices = relationship('MechtaPrices', back_populates='product')


class MechtaPrices(Base):
    __tablename__ = 'mechta_prices'
    id = Column(Integer, primary_key=True, index=True)
    created = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    price = Column(String, nullable=False)
    discount = Column(String)
    product_id = Column(Integer, ForeignKey(MechtaProducts.id))

    product = relationship('MechtaProducts', back_populates='prices')


Base.metadata.create_all(engine)
