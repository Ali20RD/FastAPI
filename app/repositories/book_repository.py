from typing import List, Optional
from sqlalchemy.orm import Session
from app.repositories.base_repository import BaseRepository
from app.models.book_model import Book
from app.models.enums import BookStatus

class BookRepository(BaseRepository[Book]):
    """Repository مخصوص کتاب‌ها"""
    
    def __init__(self, db: Session):
        super().__init__(Book, db)
    
    def get_by_author(self, author_id: int) -> List[Book]:
        return self.db.query(Book).filter(Book.author_id == author_id).all()
    
    def get_by_status(self, status: BookStatus) -> List[Book]:
        return self.db.query(Book).filter(Book.status == status).all()
    
    def get_available_books(self) -> List[Book]:
        return self.db.query(Book).filter(
            Book.status == BookStatus.AVAILABLE,
            Book.stock > 0
        ).all()
    
    def get_by_author_and_status(self, author_id: int, status: BookStatus) -> List[Book]:
        return self.db.query(Book).filter(
            Book.author_id == author_id,
            Book.status == status
        ).all()
    
    def update_stock(self, book_id: int, new_stock: int) -> Optional[Book]:
        return self.update(book_id, stock=new_stock)
    
    def update_status(self, book_id: int, new_status: BookStatus) -> Optional[Book]:
        return self.update(book_id, status=new_status)
    
    def search_books(self, query: str) -> List[Book]:
        """جستجوی کتاب بر اساس عنوان یا نویسنده"""
        return self.db.query(Book).filter(
            Book.title.ilike(f"%{query}%") | 
            Book.author_name.ilike(f"%{query}%")
        ).all()