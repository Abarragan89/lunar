from app.db import Base
from sqlalchemy import Column, Integer, String, Float, Numeric
from sqlalchemy.orm import validates
import bcrypt

salt = bcrypt.gensalt()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username_lowercase = Column(String(50), nullable=True)
    username = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    monthly_income = Column(Numeric(precision=15, scale=2), nullable=False)

    def verify_password(self, password):
        return bcrypt.checkpw(
            password.encode('utf-8'),
            self.password.encode('utf-8')
        )

    @validates('email')
    def validate_email(self, key, email):
        assert '@' in email
        return email
    
    @validates('password')
    def validate_password(self, key, password):
        assert len(password) > 5
        return bcrypt.hashpw(password.encode('utf-8'), salt)
    