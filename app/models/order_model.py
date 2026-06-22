from sqlalchemy import Column, Integer, String, Float,ForeignKey,TEXT, Enum, DateTime, JSON
from app.models.base import BaseModel
from app.models.enums import OrderStatus
from datetime import datetime
from sqlalchemy import func

class Order(BaseModel):
    __tablename__ = "orders"
    
    id = Column(Integer,primary_key=True, index=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    total_amount = Column(Float, nullable=False)
    status = Column(Enum(OrderStatus), default=OrderStatus.PENDING, nullable=False)
    shipping_address = Column(String(255), nullable=False)#ادرس رو به این ستون وصل کن 

    payment_status = Column(String(50), default="pending")

    order_date = Column(DateTime, default=func.now(), nullable=False)

    notes = Column(TEXT, nullable=True)
    
    

class OrderItem(BaseModel):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, nullable=False)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("books.id"), nullable=False)
    quantity = Column(Integer, default=1) 
    price_at_purchase = Column(Integer, nullable=False)
    




    def can_be_cancelled(self) -> bool:
        """Check if order can be cancelled"""
        return self.status in [OrderStatus.PENDING]
    
    def is_completed(self) -> bool:
        return self.status == OrderStatus.COMPLETED
    
    def update_status(self, new_status: OrderStatus) -> None:
        """Update order status"""
        self.status = new_status
        if new_status == OrderStatus.COMPLETED:
            self.completed_at = datetime.utcnow()
    
    def __repr__(self):
        return f"<Order {self.order_number} by User {self.user_id}>"