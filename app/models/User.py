from app.db import Base
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import validates
import bcrypt

salt = bcrypt.gensalt()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    monthly_income = Column(Float, nullable=False)

    @validates('email')
    def validate_email(self, key, email):
        # make sure email address contains @ character
        assert '@' in email

        return email
    
    @validates('password')
    def validate_password(self, key, password):
        assert len(password) > 8

        return bcrypt.hashpw(password.encode('utf-8'), salt)