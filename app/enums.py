# enums.py
from enum import Enum

class UserRole(str, Enum):
    ADMIN = "admin"
    AUTHOR = "author"
    USER = "user"

class OrderStatus(str, Enum):
    PENDING = "pending"
    PAID = "paid"
    SHIPPED = "shipped"
    CANCELLED = "cancelled"