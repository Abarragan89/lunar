from app.db import Base
from sqlalchemy import Column, Integer, ForeignKey, Numeric, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

class ActiveSalary(Base):
    __tablename__ = 'active_salary'
    id = Column(Integer, primary_key=True)
    salary_amount = Column(Numeric(precision=15, scale=2), nullable=False)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    start_date = Column(Integer, nullable=False)
    is_active = Column(Integer, default=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)

    user = relationship('User')