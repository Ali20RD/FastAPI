from typing import List, Optional
from sqlalchemy.orm import Session
from app.repositories.base_repository import BaseRepository
from app.models.order_model import Order
from app.models.enums import OrderStatus

class OrderRepository(BaseRepository[Order]):
    """Repository مخصوص سفارشات"""
    
    def __init__(self, db: Session):
        super().__init__(Order, db)
    
    def get_by_user(self, user_id: int) -> List[Order]:
        return self.db.query(Order).filter(Order.user_id == user_id).all()
    
    def get_by_status(self, status: OrderStatus) -> List[Order]:
        return self.db.query(Order).filter(Order.status == status).all()
    
    def get_by_order_number(self, order_number: str) -> Optional[Order]:
        return self.db.query(Order).filter(Order.order_number == order_number).first()
    
    def update_status(self, order_id: int, new_status: OrderStatus) -> Optional[Order]:
        return self.update(order_id, status=new_status)
    
    def get_user_orders(self, user_id: int) -> List[Order]:
        return self.db.query(Order).filter(Order.user_id == user_id).all()