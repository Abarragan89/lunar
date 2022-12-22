from app.db import Base
from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, DateTime, Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    description = Column(String(50), nullable=False, default='')
    monthly_bill = Column(Boolean, nullable=True)
    amount = Column(Numeric(precision=15, scale=2), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    tag_id = Column(Integer, ForeignKey('tags.id', ondelete='CASCADE'), nullable=False)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())

    user = relationship('User')
    tag = relationship('Tag')