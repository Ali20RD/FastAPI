from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.book_service import BookService
from app.services.permission_service import PermissionService
from app.views.book_schemas import (
    BookCreate, BookUpdate, BookStockUpdate, 
    BookStatusUpdate, BookResponse, BookWithAvailability
)
from app.dependencies.auth_deps import get_current_user, require_permission
from app.models.user_model import User

router = APIRouter(prefix="/books", tags=["Books"])

@router.get("/", response_model=List[BookWithAvailability])
async def get_books(
    search: str = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """دریافت کتاب‌ها بر اساس دسترسی کاربر"""
    permission_service = PermissionService(db)
    books = permission_service.get_visible_books(current_user)
    
    # جستجو اگر پارامتر داده شده باشد
    if search:
        book_service = BookService(db)
        books = book_service.search_books(search)
        # فیلتر بر اساس دسترسی
        visible_ids = [b.id for b in permission_service.get_visible_books(current_user)]
        books = [b for b in books if b.id in visible_ids]
    
    return [BookWithAvailability.from_book(book) for book in books]

@router.get("/available", response_model=List[BookResponse])
async def get_available_books(
    db: Session = Depends(get_db)
):
    """دریافت کتاب‌های موجود (بدون نیاز به لاگین)"""
    book_service = BookService(db)
    books = book_service.get_available_books()
    return books

@router.get("/{book_id}", response_model=BookWithAvailability)
async def get_book(
    book_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """دریافت یک کتاب خاص"""
    book_service = BookService(db)
    book = book_service.get_by_id(book_id)
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )
    
    # بررسی دسترسی
    permission_service = PermissionService(db)
    visible_books = permission_service.get_visible_books(current_user)
    if book.id not in [b.id for b in visible_books]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to view this book"
        )
    
    return BookWithAvailability.from_book(book)

@router.post("/", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
async def create_book(
    book_data: BookCreate,
    current_user: User = Depends(require_permission("book:create")),
    db: Session = Depends(get_db)
):
    """ایجاد کتاب جدید (فقط نویسنده و ادمین)"""
    book_service = BookService(db)
    
    # بررسی اینکه کاربر نویسنده است (اگر ادمین نیست)
    if not current_user.is_admin() and not current_user.is_author():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only authors and admins can create books"
        )
    
    try:
        book = book_service.create_book(
            title=book_data.title,
            description=book_data.description,
            author_id=current_user.id,
            author_name=current_user.full_name or current_user.username,
            price=book_data.price,
            isbn=book_data.isbn,
            published_year=book_data.published_year,
            stock=book_data.stock
        )
        return book
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.put("/{book_id}", response_model=BookResponse)
async def update_book(
    book_id: int,
    book_data: BookUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """بروزرسانی کتاب"""
    book_service = BookService(db)
    permission_service = PermissionService(db)
    
    # بررسی دسترسی
    can_manage, message = permission_service.can_manage_book(current_user, book_id)
    if not can_manage:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=message
        )
    
    updated_book = book_service.update_book(book_id, **book_data.dict(exclude_unset=True))
    if not updated_book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )
    return updated_book

@router.patch("/{book_id}/stock", response_model=BookResponse)
async def update_book_stock(
    book_id: int,
    stock_data: BookStockUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """بروزرسانی موجودی کتاب"""
    book_service = BookService(db)
    permission_service = PermissionService(db)
    
    # بررسی دسترسی
    can_update, message = permission_service.can_update_stock(current_user, book_id)
    if not can_update:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=message
        )
    
    updated_book = book_service.update_stock(book_id, stock_data.stock)
    if not updated_book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )
    return updated_book

@router.patch("/{book_id}/status", response_model=BookResponse)
async def update_book_status(
    book_id: int,
    status_data: BookStatusUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """بروزرسانی وضعیت کتاب (موجود/ناموجود)"""
    book_service = BookService(db)
    permission_service = PermissionService(db)
    
    # بررسی دسترسی
    can_manage, message = permission_service.can_manage_book(current_user, book_id)
    if not can_manage:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=message
        )
    
    updated_book = book_service.update_status(book_id, status_data.status)
    if not updated_book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )
    return updated_book

@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(
    book_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """حذف کتاب (تغییر وضعیت به Archived)"""
    book_service = BookService(db)
    permission_service = PermissionService(db)
    
    # بررسی دسترسی
    can_manage, message = permission_service.can_manage_book(current_user, book_id)
    if not can_manage:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=message
        )
    
    if not book_service.delete_book(book_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )