# from pydantic import BaseModel, EmailStr
# from typing import Optional
# from datetime import datetime
# from app.enums import UserRole  # در user_schema.py
# from app.enums import OrderStatus  # در order_schema.py
# class UserBase(BaseModel):
#     username: str
#     email: EmailStr
#     role: UserRole


# class UserCreate(BaseModel):
#     username: str
#     email: EmailStr
#     password: str   # plain password from client


# class UserUpdate(BaseModel):
#     username: Optional[str] = None
#     email: Optional[EmailStr] = None
#     password: Optional[str] = None
#     role: Optional[UserRole] = None


# class UserOut(BaseModel):
#     id: int
#     username: str
#     email: EmailStr
#     role: UserRole
#     created_at: datetime

#     class Config:
#         from_attributes  = True






# app/schemas/user_schema.py
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from app.enums import UserRole

class UserBase(BaseModel):
    username: str
    email: EmailStr
    role: UserRole

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    role: Optional[UserRole] = None

class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: UserRole
    created_at: datetime

    class Config:
        from_attributes = True