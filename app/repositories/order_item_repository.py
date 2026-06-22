from typing import List
from sqlalchemy.orm import Session
from app.repositories.base_repository import BaseRepository
from app.models.order_model import OrderItem

class OrderItemRepository(BaseRepository[OrderItem]):
    """Repository مخصوص آیتم‌های سفارش"""
    
    def __init__(self, db: Session):
        super().__init__(OrderItem, db)
    
    def get_by_order(self, order_id: int) -> List[OrderItem]:
        return self.db.query(OrderItem).filter(OrderItem.order_id == order_id).all()
    
    def get_by_book(self, book_id: int) -> List[OrderItem]:
        return self.db.query(OrderItem).filter(OrderItem.book_id == book_id).all()