
from sqlalchemy import Column, Integer, String, Boolean, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    description = Column(String, index=True)
    price = Column(Numeric(10, 2), nullable=False) 
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    is_available = Column(Boolean, default=True, nullable=False)
    stock_quantity = Column(Integer, default=0, nullable=False)

    author = relationship("User", back_populates="books")
    orders = relationship("Order", back_populates="book")