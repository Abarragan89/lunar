from app.db import Base
from sqlalchemy import Column, Integer, String, Numeric
from sqlalchemy.orm import validates

class TempUser(Base):
    __tablename__ = 'temp_users'
    id = Column(Integer, primary_key=True)
    username_lowercase = Column(String(50))
    username = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False)
    unique_id = Column(String(50), nullable=False, unique=True)
    prefixes=['TEMPORARY']

    @validates('email')
    def validate_email(self, key, email):
        assert '@' in email
        return email
    