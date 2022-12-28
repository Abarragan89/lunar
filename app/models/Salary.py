from app.db import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Numeric, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

class Salary(Base):
    __tablename__ = 'salary'
    id = Column(Integer, primary_key=True)
    salary_amount = Column(Numeric(precision=15, scale=2), nullable=False)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)

    user = relationship('User')