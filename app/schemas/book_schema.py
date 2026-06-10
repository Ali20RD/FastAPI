from pydantic import BaseModel, condecimal
from typing import Optional
from decimal import Decimal

class BookBase(BaseModel):
    title: str
    description: Optional[str] = None
    price: condecimal(max_digits=10, decimal_places=2)
    stock_quantity: int
    is_available: bool = True


class BookCreate(BookBase):
   
    author_id: Optional[int] = None


class BookUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[condecimal(max_digits=10, decimal_places=2)] = None
    stock_quantity: Optional[int] = None
    is_available: Optional[bool] = None



class BookOut(BaseModel):
    id: int
    title: str
    description: Optional[str]
    price: Decimal
    stock_quantity: int
    is_available: bool
    author_id: int

    class Config:
        from_attributes = True  # Pydantic v2
 
