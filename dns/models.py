from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, func
from sqlalchemy.orm import relationship

from database import Base, engine


class DnsProducts(Base):
    __tablename__ = 'dns_products'
    id = Column(Integer, primary_key=True, index=True)
    created = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    name = Column(String, nullable=False)
    url = Column(String, nullable=False)
    store_id = Column(String, nullable=False)
    store_code = Column(String, nullable=False)
    category = Column(String, nullable=False)
    characteristics = Column(String)
    images = Column(String, nullable=False)

    prices = relationship('DnsPrices', back_populates='product')


class DnsPrices(Base):
    __tablename__ = 'dns_prices'
    id = Column(Integer, primary_key=True, index=True)
    created = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    price = Column(String, nullable=False)
    discount = Column(String)
    product_id = Column(Integer, ForeignKey(DnsProducts.id))

    product = relationship('DnsProducts', back_populates='prices')


Base.metadata.create_all(engine)
