# from pydantic import BaseModel, condecimal
# from typing import Optional, List
# from decimal import Decimal




# class BookBase(BaseModel):
#     title: str
#     description: Optional[str] = None
    

# class BookCreate(BookBase):
#     author_ids: List[int]
#     price: int
#     isbn: int
#     stock_quantity: int

# class AuthorShortOut(BaseModel):
#     id: int
#     username: str
#     email: str

#     class Config:
#         from_attributes = True

# class BookOut(BookBase):
#     id: int
#     authors: List[AuthorShortOut] = []  # نمایش کامل اطلاعات نویسندگان کتاب
#     price: int
#     class Config:
#         from_attributes = True

# class BookEdit(BookBase):
#     stock_quantity: Optional[int] = None
#     price: Optional[int] = None




from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field
from app.models.enums import BookStatus

# ===== Base =====
class BookBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    price: float = Field(..., ge=0)
    isbn: Optional[str] = None
    published_year: Optional[int] = Field(None, ge=1000, le=datetime.now().year)
    stock: int = Field(0, ge=0)

# ===== Create =====
class BookCreate(BookBase):
    pass

# ===== Update =====
class BookUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    price: Optional[float] = Field(None, ge=0)
    isbn: Optional[str] = None
    published_year: Optional[int] = Field(None, ge=1000, le=datetime.now().year)
    status: Optional[BookStatus] = None

# ===== Stock Update =====
class BookStockUpdate(BaseModel):
    stock: int = Field(..., ge=0)

class BookStatusUpdate(BaseModel):
    status: BookStatus

# ===== Response =====
class BookResponse(BookBase):
    id: int
    author_id: int
    author_name: str
    status: BookStatus
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True

class BookWithAvailability(BookResponse):
    is_available: bool
    
    @classmethod
    def from_book(cls, book):
        return cls(
            **book.__dict__,
            is_available=book.is_available()
        )