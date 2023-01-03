from app.db import Base
from sqlalchemy import Column, Integer, String, Numeric
from sqlalchemy.orm import validates

class TempUser(Base):
    __tablename__ = 'temp_users'
    id = Column(Integer, primary_key=True)
    username_lowercase = Column(String(50))
    username = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    salary_amount = Column(Numeric(precision=15, scale=2), nullable=False)
    prefixes=['TEMPORARY']

    @validates('email')
    def validate_email(self, key, email):
        assert '@' in email
        return email
    
    @validates('password')
    def validate_password(self, key, password):
        assert len(password) > 5
        return password
    