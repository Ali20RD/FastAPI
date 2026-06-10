
from pydantic import BaseModel, conint
from datetime import datetime
from typing import Optional
from decimal import Decimal
from app.enums import OrderStatus
from app.schemas.book_schema import BookOut

class OrderBase(BaseModel):
    quantity: conint(ge=1)

class OrderCreate(BaseModel):
    book_id: int
    quantity: conint(ge=1) = 1

class OrderUpdate(BaseModel):
    status: Optional[OrderStatus] = None
    quantity: Optional[conint(ge=1)] = None

class OrderOut(BaseModel):
    id: int
    order_date: datetime
    status: OrderStatus
    quantity: int
    total_price: Decimal
    user_id: int
    book_id: int
    book: BookOut

    class Config:
        from_attributes = True