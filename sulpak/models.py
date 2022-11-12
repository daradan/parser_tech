from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, func
from sqlalchemy.orm import relationship

from database import Base, engine


class SulpakProducts(Base):
    __tablename__ = 'sulpak_products'
    id = Column(Integer, primary_key=True, index=True)
    created = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    name = Column(String, nullable=False)
    url = Column(String, nullable=False)
    store_id = Column(String, nullable=False)
    brand = Column(String, nullable=False)
    category = Column(String, nullable=False)
    characteristics = Column(String, nullable=False)
    images = Column(String, nullable=False)

    prices = relationship('SulpakPrices', back_populates='product')


class SulpakPrices(Base):
    __tablename__ = 'sulpak_prices'
    id = Column(Integer, primary_key=True, index=True)
    created = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    price = Column(String, nullable=False)
    discount = Column(String)
    product_id = Column(Integer, ForeignKey(SulpakProducts.id))

    product = relationship('SulpakProducts', back_populates='prices')


Base.metadata.create_all(engine)
