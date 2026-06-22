from typing import Optional, List
from sqlalchemy.orm import Session
from app.repositories.book_repository import BookRepository
from app.models.book_model import Book
from app.models.enums import BookStatus
from app.services.permission_service import PermissionService

class BookService:
    """سرویس مدیریت کتاب‌ها"""
    
    def __init__(self, db: Session):
        self.db = db
        self.repository = BookRepository(db)
        self.permission_service = PermissionService(db)
    
    def create_book(self, title: str, description: str, author_id: int, 
                   author_name: str, price: float, isbn: str = None, 
                   published_year: int = None, stock: int = 0) -> Book:
        """ایجاد کتاب جدید"""
        return self.repository.create(
            title=title,
            description=description,
            author_id=author_id,
            author_name=author_name,
            price=price,
            isbn=isbn,
            published_year=published_year,
            stock=stock,
            status=BookStatus.AVAILABLE if stock > 0 else BookStatus.UNAVAILABLE
        )
    
    def get_by_id(self, book_id: int) -> Optional[Book]:
        return self.repository.get_by_id(book_id)
    
    def get_all_books(self, skip: int = 0, limit: int = 100) -> List[Book]:
        return self.repository.get_all(skip, limit)
    
    def get_available_books(self) -> List[Book]:
        return self.repository.get_available_books()
    
    def get_by_author(self, author_id: int) -> List[Book]:
        return self.repository.get_by_author(author_id)
    
    def update_book(self, book_id: int, **kwargs) -> Optional[Book]:
        """بروزرسانی کتاب"""
        return self.repository.update(book_id, **kwargs)
    
    def update_stock(self, book_id: int, new_stock: int) -> Optional[Book]:
        """بروزرسانی موجودی کتاب"""
        book = self.repository.get_by_id(book_id)
        if not book:
            return None
        
        # اگر موجودی به صفر رسید، وضعیت تغییر می‌کند
        status = BookStatus.AVAILABLE if new_stock > 0 else BookStatus.UNAVAILABLE
        
        return self.repository.update(book_id, stock=new_stock, status=status)
    
    def update_status(self, book_id: int, new_status: BookStatus) -> Optional[Book]:
        """بروزرسانی وضعیت کتاب"""
        return self.repository.update_status(book_id, new_status)
    
    def delete_book(self, book_id: int) -> bool:
        """حذف کتاب (منطقی: تغییر وضعیت به Archived)"""
        book = self.repository.get_by_id(book_id)
        if not book:
            return False
        
        return self.repository.update_status(book_id, BookStatus.ARCHIVED) is not None
    
    def search_books(self, query: str) -> List[Book]:
        """جستجوی کتاب"""
        return self.repository.search_books(query)
    
    def reduce_stock(self, book_id: int, quantity: int) -> Optional[Book]:
        """کاهش موجودی کتاب (برای خرید)"""
        book = self.repository.get_by_id(book_id)
        if not book:
            return None
        
        if book.stock < quantity:
            raise ValueError("Not enough stock available")
        
        new_stock = book.stock - quantity
        return self.update_stock(book_id, new_stock)