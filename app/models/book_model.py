from sqlalchemy import Column, Integer, String, Text, Float, Enum, ForeignKey, Boolean, DateTime
from app.models.base import BaseModel
from app.models.enums import BookStatus
from sqlalchemy import func
from datetime import datetime

class Book(BaseModel):
    __tablename__ = "books"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False, index=True)
    description = Column(Text)
    author_id = Column(Integer,ForeignKey("users.id") ,nullable=False)
    author_name = Column(String(100), nullable=False)
    price = Column(Integer, nullable=False)
    isbn = Column(String(20), unique=True, nullable=True)
    status = Column(Enum(BookStatus), default=BookStatus.AVAILABLE, nullable=False)
    stock_quantity = Column(Integer, default=1, nullable=False)
    published_date = Column(DateTime, default=func.now())
    is_active = Column(Boolean, default=True, nullable=False)
    



    def is_available(self) -> bool:
        """Check if book is available for purchase"""
        return self.status == BookStatus.AVAILABLE and self.stock_quantity > 0
    
    def can_purchase(self, quantity: int = 1) -> bool:
        """Check if book can be purchased in given quantity"""
        return self.is_available() and self.stock_quantity >= quantity
    
    def reduce_stock(self, quantity: int = 1) -> bool:
        """Reduce stock quantity"""
        if self.stock_quantity >= quantity:
            self.stock_quantity -= quantity
            if self.stock_quantity == 0:
                self.status = BookStatus.OUT_OF_STOCK
            return True
        return False
    
    def restock(self, quantity: int) -> None:
        """Restock book"""
        self.stock_quantity += quantity
        if self.status == BookStatus.OUT_OF_STOCK:
            self.status = BookStatus.AVAILABLE
    
    def mark_unavailable(self) -> None:
        """Mark book as unavailable"""
        self.status = BookStatus.UNAVAILABLE
    
    def __repr__(self):
        return f"<Book {self.title} by {self.author_name}>"