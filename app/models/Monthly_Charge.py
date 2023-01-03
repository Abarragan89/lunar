from app.db import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.ext.hybrid import hybrid_property


class MonthlyCharge(Base):
    __tablename__ = 'monthly_charge'
    id = Column(Integer, primary_key=True)
    description = Column(String(50), nullable=False, default='')
    amount = Column(Numeric(precision=15, scale=2), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    tag_id = Column(Integer, ForeignKey('tags.id', ondelete='CASCADE'), nullable=False)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    start_date = Column(Integer, nullable=False)


    user = relationship('User')
    tag = relationship('Tag')