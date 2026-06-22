from typing import Optional, List, Tuple
from datetime import datetime
import uuid
from sqlalchemy.orm import Session
from app.repositories.order_repository import OrderRepository
from app.repositories.order_item_repository import OrderItemRepository
from app.repositories.book_repository import BookRepository
from app.models.order_model import Order
from app.models.order_model import OrderItem
from app.models.book_model import Book
from app.models.enums import OrderStatus, BookStatus
from app.services.book_service import BookService
from app.services.permission_service import PermissionService

class OrderService:
    """سرویس مدیریت سفارشات"""
    
    def __init__(self, db: Session):
        self.db = db
        self.order_repo = OrderRepository(db)
        self.order_item_repo = OrderItemRepository(db)
        self.book_repo = BookRepository(db)
        self.book_service = BookService(db)
        self.permission_service = PermissionService(db)
    
    def generate_order_number(self) -> str:
        """تولید شماره سفارش یکتا"""
        return f"ORD-{uuid.uuid4().hex[:8].upper()}"
    
    def create_order(self, user_id: int, user_email: str, 
                    books: List[dict], shipping_address: str) -> Order:
        """
        ایجاد سفارش جدید
        books: لیست دیکشنری‌های {'book_id': int, 'quantity': int}
        """
        if not books:
            raise ValueError("Order must contain at least one book")
        
        total_amount = 0.0
        order_items_data = []
        
        # بررسی موجودی و محاسبه قیمت
        for item in books:
            book_id = item['book_id']
            quantity = item['quantity']
            
            book = self.book_repo.get_by_id(book_id)
            if not book:
                raise ValueError(f"Book with ID {book_id} not found")
            
            if not book.is_available():
                raise ValueError(f"Book '{book.title}' is not available")
            
            if book.stock < quantity:
                raise ValueError(f"Not enough stock for book '{book.title}'. Available: {book.stock}")
            
            total_amount += book.price * quantity
            
            order_items_data.append({
                'book_id': book_id,
                'book_title': book.title,
                'quantity': quantity,
                'price_at_time': book.price
            })
        
        # ایجاد سفارش
        order_number = self.generate_order_number()
        order = self.order_repo.create(
            order_number=order_number,
            user_id=user_id,
            user_email=user_email,
            total_amount=total_amount,
            status=OrderStatus.PENDING,
            shipping_address=shipping_address
        )
        
        # ایجاد آیتم‌های سفارش
        for item_data in order_items_data:
            self.order_item_repo.create(
                order_id=order.id,
                book_id=item_data['book_id'],
                book_title=item_data['book_title'],
                quantity=item_data['quantity'],
                price_at_time=item_data['price_at_time']
            )
            
            # کاهش موجودی کتاب
            book = self.book_repo.get_by_id(item_data['book_id'])
            self.book_service.reduce_stock(book.id, item_data['quantity'])
        
        return order
    
    def get_order_by_id(self, order_id: int) -> Optional[Order]:
        return self.order_repo.get_by_id(order_id)
    
    def get_order_by_number(self, order_number: str) -> Optional[Order]:
        return self.order_repo.get_by_order_number(order_number)
    
    def get_user_orders(self, user_id: int) -> List[Order]:
        return self.order_repo.get_user_orders(user_id)
    
    def get_order_items(self, order_id: int) -> List[OrderItem]:
        return self.order_item_repo.get_by_order(order_id)
    
    def update_order_status(self, order_id: int, new_status: OrderStatus) -> Optional[Order]:
        """بروزرسانی وضعیت سفارش"""
        order = self.order_repo.get_by_id(order_id)
        if not order:
            return None
        
        # اگر سفارش کامل شد، زمان تکمیل ثبت می‌شود
        if new_status == OrderStatus.COMPLETED:
            return self.order_repo.update(order_id, status=new_status, completed_at=datetime.utcnow())
        
        return self.order_repo.update_status(order_id, new_status)
    
    def cancel_order(self, order_id: int) -> Optional[Order]:
        """لغو سفارش و بازگرداندن موجودی"""
        order = self.order_repo.get_by_id(order_id)
        if not order:
            return None
        
        if order.status in [OrderStatus.COMPLETED, OrderStatus.DELIVERED]:
            raise ValueError("Cannot cancel completed or delivered order")
        
        # بازگرداندن موجودی کتاب‌ها
        items = self.order_item_repo.get_by_order(order_id)
        for item in items:
            book = self.book_repo.get_by_id(item.book_id)
            if book:
                self.book_service.update_stock(book.id, book.stock + item.quantity)
        
        return self.order_repo.update_status(order_id, OrderStatus.CANCELLED)
    
    def get_all_orders(self, skip: int = 0, limit: int = 100) -> List[Order]:
        """دریافت همه سفارشات (فقط ادمین)"""
        return self.order_repo.get_all(skip, limit)
    
    def get_visible_orders(self, user) -> List[Order]:
        """دریافت سفارشات بر اساس دسترسی کاربر"""
        if user.is_admin():
            return self.order_repo.get_all()
        else:
            return self.order_repo.get_user_orders(user.id)