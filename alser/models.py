from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, func
from sqlalchemy.orm import relationship

from database import Base, engine


class AlserProducts(Base):
    __tablename__ = 'alser_products'
    id = Column(Integer, primary_key=True, index=True)
    created = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    name = Column(String, nullable=False)
    url = Column(String, nullable=False)
    store_id = Column(String, nullable=False)
    brand = Column(String, nullable=False)
    category = Column(String, nullable=False)
    characteristics = Column(String, nullable=False)
    images = Column(String, nullable=False)

    prices = relationship('AlserPrices', back_populates='product')


class AlserPrices(Base):
    __tablename__ = 'alser_prices'
    id = Column(Integer, primary_key=True, index=True)
    created = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    price = Column(String, nullable=False)
    discount = Column(String)
    product_id = Column(Integer, ForeignKey(AlserProducts.id))

    product = relationship('AlserProducts', back_populates='prices')


Base.metadata.create_all(engine)
