
from sqlalchemy import Column, Integer, String, DateTime, Numeric, ForeignKey, Enum as SQLAlchemyEnum
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime
from enum import Enum as pyEnum
from sqlalchemy import func




class OrderStatus(str, pyEnum):
    
    PENDING = "pending"
    COMPLETED = "completed"
    SHIPPED = "shipped"
    CANCELLED = "cancelled"

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    order_date = Column(DateTime, default=func.now())
    status = Column(SQLAlchemyEnum(OrderStatus, name="order_status"), default=OrderStatus.PENDING)
    quantity = Column(Integer, default=1, nullable=False) # تعداد کتاب در این سفارش
    total_price = Column(Numeric(12, 2), nullable=False) # قیمت کل سفارش (quantity * book.price)


    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)

    user = relationship("User", back_populates="orders") 
    book = relationship("Book", back_populates="orders")

