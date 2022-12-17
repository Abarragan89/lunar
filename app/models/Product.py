from app.db import Base
from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship


class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    product_name = Column(String(50), nullable=False)
    monthly_bill = Column(Boolean, nullable=True)
    price = Column(Float, nullable=False)

    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    tag_id = Column(Integer, ForeignKey('tags.id'), nullable=False)

    user = relationship('User')
    tag = relationship('Tag')


