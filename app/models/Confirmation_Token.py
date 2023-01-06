from app.db import Base
from sqlalchemy import Column, Integer, String


class ConfirmationToken(Base):
    __tablename__ = 'confirmation_token'
    id = Column(Integer, primary_key=True)
    unique_string = Column(String(50), unique=True)
    email = Column(String(50), nullable=False)
    prefixes=['TEMPORARY']
