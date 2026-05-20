from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum as SQLAlchemyEnum
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime
from enum import Enum as pyEnum
from sqlalchemy import func



order_date = Column(DateTime, default=func.now())

class UserRole(str,pyEnum):
    
    ADMIN = "admin"
    AUTHOR = "author"
    USER = "user"


class User(Base):
    
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)  
    created_at = Column(DateTime, default=func.now())
    otp_secret = Column(String, nullable=True)
    
    role = Column(SQLAlchemyEnum(UserRole, name="user_role"), default=UserRole.USER, nullable=False)
    
    
    
    
    books = relationship("Book", back_populates="author", cascade="all, delete")
    orders = relationship("Order", back_populates="user", cascade="all, delete")
