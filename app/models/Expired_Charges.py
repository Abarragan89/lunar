from app.db import Base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class ExpiredCharges(Base):
    __tablename__ = 'expired_charges'
    id = Column(Integer, primary_key=True)
    description = Column(String(50), nullable=False, default='')
    amount = Column(Numeric(precision=15, scale=2), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    tag_id = Column(Integer, ForeignKey('tags.id', ondelete='CASCADE'), nullable=False)
    # expiration_limit is integer made up of the year and month as a single number. 
    # this number will be used to determine if it should be used with in a query with < > signs
    expiration_limit = Column(Integer, nullable=False)
    start_date = Column(Integer, nullable=False)
    time_created = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship('User')
    tag = relationship('Tag')