# from pydantic import BaseModel, conint
# from datetime import datetime
# from decimal import Decimal
# from app.models.enums import OrderStatus, PaymentStatus
# from typing import Optional

# class OrderCreate(BaseModel):
#     book_id: int
#     quantity: conint(ge=1) = 1


# class OrderUpdate(BaseModel):
#     status: Optional[OrderStatus] = None
#     quantity: Optional[conint(ge=1)] = None


# class OrderOut(BaseModel):
#     id: int
#     order_date: datetime
#     status: OrderStatus
#     quantity: int
#     total_price: Decimal
#     user_id: int
#     payment_status: PaymentStatus = PaymentStatus.PENDING
#     class Config:
#         from_attributes = True

        

from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field
from app.models.enums import OrderStatus

# ===== Order Item =====
class OrderItemCreate(BaseModel):
    book_id: int
    quantity: int = Field(..., ge=1)

class OrderItemResponse(BaseModel):
    id: int
    book_id: int
    book_title: str
    quantity: int
    price_at_time: float
    created_at: datetime
    
    class Config:
        orm_mode = True

# ===== Order =====
class OrderCreate(BaseModel):
    books: List[OrderItemCreate] = Field(..., min_items=1)
    shipping_address: str

class OrderUpdate(BaseModel):
    status: OrderStatus

class OrderResponse(BaseModel):
    id: int
    order_number: str
    user_id: int
    user_email: str
    total_amount: float
    status: OrderStatus
    shipping_address: Optional[str]
    notes: Optional[str]
    created_at: datetime
    updated_at: datetime
    completed_at: Optional[datetime]
    
    class Config:
        orm_mode = True

class OrderDetailResponse(OrderResponse):
    items: List[OrderItemResponse]
    
    @classmethod
    def from_order(cls, order, items):
        return cls(
            **order.__dict__,
            items=items
        )