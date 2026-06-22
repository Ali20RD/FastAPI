from typing import Optional, Tuple
from sqlalchemy.orm import Session
from app.models.user_model import User
from app.models.book_model import Book
from app.models.enums import UserRole
from app.repositories.user_repository import UserRepository
from app.repositories.book_repository import BookRepository

class PermissionService:
    """سرویس مدیریت دسترسی‌ها"""
    
    def __init__(self, db: Session):
        self.db = db
        self.user_repo = UserRepository(db)
        self.book_repo = BookRepository(db)
    
    # ============ بررسی دسترسی‌های عمومی ============
    
    def has_permission(self, user: User, permission: str) -> bool:
        """بررسی دسترسی کاربر به یک مجوز"""
        if not user or not user.is_active:
            return False
        return user.has_permission(permission)
    
    # ============ بررسی دسترسی به کتاب ============
    
    def can_manage_book(self, user: User, book_id: int) -> Tuple[bool, str]:
        """بررسی اینکه کاربر می‌تواند کتاب را مدیریت کند"""
        if not user or not user.is_active:
            return False, "User not active"
        
        book = self.book_repo.get_by_id(book_id)
        if not book:
            return False, "Book not found"
        
        # ادمین می‌تواند همه کتاب‌ها را مدیریت کند
        if user.is_admin():
            return True, "Admin can manage all books"
        
        # نویسنده فقط کتاب‌های خودش را می‌تواند مدیریت کند
        if user.is_author() and book.author_id == user.id:
            return True, "Author can manage own books"
        
        return False, "You don't have permission to manage this book"
    
    def can_update_stock(self, user: User, book_id: int) -> Tuple[bool, str]:
        """بررسی اینکه کاربر می‌تواند موجودی کتاب را تغییر دهد"""
        if not user or not user.is_active:
            return False, "User not active"
        
        book = self.book_repo.get_by_id(book_id)
        if not book:
            return False, "Book not found"
        
        # ادمین می‌تواند موجودی همه کتاب‌ها را تغییر دهد
        if user.is_admin():
            return True, "Admin can update any stock"
        
        # نویسنده فقط موجودی کتاب‌های خودش را می‌تواند تغییر دهد
        if user.is_author() and book.author_id == user.id:
            return True, "Author can update own book stock"
        
        return False, "You don't have permission to update stock for this book"
    
    def can_purchase_book(self, user: User, book_id: int) -> Tuple[bool, str]:
        """بررسی اینکه کاربر می‌تواند کتاب را بخرد"""
        if not user or not user.is_active:
            return False, "User not active"
        
        book = self.book_repo.get_by_id(book_id)
        if not book:
            return False, "Book not found"
        
        if not book.is_available():
            return False, "Book is not available for purchase"
        
        # فقط کاربران معمولی و ادمین می‌توانند خرید کنند
        # (نویسنده هم می‌تواند کتاب بخرد)
        if user.is_user() or user.is_admin() or user.is_author():
            return True, "User can purchase this book"
        
        return False, "You don't have permission to purchase books"
    
    # ============ بررسی دسترسی به سفارش ============
    
    def can_view_order(self, user: User, order_id: int) -> Tuple[bool, str]:
        """بررسی اینکه کاربر می‌تواند سفارش را ببیند"""
        if not user or not user.is_active:
            return False, "User not active"
        
        from app.repositories.order_repository import OrderRepository
        order_repo = OrderRepository(self.db)
        order = order_repo.get_by_id(order_id)
        
        if not order:
            return False, "Order not found"
        
        # ادمین می‌تواند همه سفارشات را ببیند
        if user.is_admin():
            return True, "Admin can view all orders"
        
        # کاربر فقط سفارشات خودش را می‌بیند
        if order.user_id == user.id:
            return True, "User can view own orders"
        
        return False, "You don't have permission to view this order"
    
    # ============ متدهای کمکی ============
    
    def get_visible_books(self, user: User) -> list:
        """دریافت کتاب‌هایی که کاربر می‌تواند ببیند"""
        if user.is_admin():
            # ادمین همه کتاب‌ها را می‌بیند
            return self.book_repo.get_all()
        elif user.is_author():
            # نویسنده کتاب‌های خودش و کتاب‌های موجود را می‌بیند
            own_books = self.book_repo.get_by_author(user.id)
            available_books = self.book_repo.get_available_books()
            # ترکیب و حذف تکراری‌ها
            all_books = own_books + [b for b in available_books if b.id not in [ob.id for ob in own_books]]
            return all_books
        else:
            # کاربر معمولی فقط کتاب‌های موجود را می‌بیند
            return self.book_repo.get_available_books()