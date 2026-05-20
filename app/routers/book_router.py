# # app/routers/book_router.py
# from fastapi import APIRouter, Depends, HTTPException, status
# from sqlalchemy.orm import Session
# from typing import List
# from app import models, schemas
# from app.database import get_db

# router = APIRouter(
#     prefix="/books",
#     tags=["Books"]
# )

# @router.post("/", response_model=schemas.BookOut, status_code=status.HTTP_201_CREATED)
# def create_book(book: schemas.BookCreate, db: Session = Depends(get_db), current_user_id: int = 1):
#     # فرض بر این است که شناسه نویسنده/کاربر فعلی از توکن گرفته می‌شود، فعلا مقدار ثابت 1 قرار می‌دهیم.
#     # ابتدا بررسی می‌کنیم کاربری که می‌خواهد کتاب ثبت کند وجود دارد یا خیر
#     author = db.query(models.User).filter(models.User.id == current_user_id).first()
#     if not author:
#         raise HTTPException(status_code=404, detail="نویسنده/کاربر معتبر یافت نشد")

#     new_book = models.Book(
#         title=book.title,
#         description=book.description,
#         price=book.price,
#         stock_quantity=book.stock_quantity,
#         is_available=book.is_available,
#         author_id=current_user_id
#     )
    
#     db.add(new_book)
#     db.commit()
#     db.refresh(new_book)
#     return new_book

# @router.get("/", response_model=List[schemas.BookOut])
# def get_books(db: Session = Depends(get_db)):
#     books = db.query(models.Book).all()
#     return books

# @router.get("/{book_id}", response_model=schemas.BookOut)
# def get_book(book_id: int, db: Session = Depends(get_db)):
#     book = db.query(models.Book).filter(models.Book.id == book_id).first()
#     if not book:
#         raise HTTPException(status_code=404, detail="کتاب مورد نظر یافت نشد")
#     return book

# @router.patch("/{book_id}", response_model=schemas.BookOut)
# def update_book(book_id: int, update_data: schemas.BookUpdate, db: Session = Depends(get_db)):
#     book = db.query(models.Book).filter(models.Book.id == book_id).first()
#     if not book:
#         raise HTTPException(status_code=404, detail="کتاب مورد نظر یافت نشد")

#     if update_data.title is not None:
#         book.title = update_data.title
#     if update_data.description is not None:
#         book.description = update_data.description
#     if update_data.price is not None:
#         book.price = update_data.price
#     if update_data.stock_quantity is not None:
#         book.stock_quantity = update_data.stock_quantity
#         # اگر موجودی صفر شد، وضعیت موجود بودن را خودکار غیرفعال می‌کنیم
#         if update_data.stock_quantity == 0:
#             book.is_available = False
#     if update_data.is_available is not None:
#         book.is_available = update_data.is_available

#     db.commit()
#     db.refresh(book)
#     return book

# @router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
# def delete_book(book_id: int, db: Session = Depends(get_db)):
#     book = db.query(models.Book).filter(models.Book.id == book_id).first()
#     if not book:
#         raise HTTPException(status_code=404, detail="کتاب مورد نظر یافت نشد")

#     db.delete(book)
#     db.commit()
#     return










# app/routers/book_router.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app import models, schemas
from app.database import get_db

router = APIRouter(prefix="/books", tags=["Books"])

@router.post("/", response_model=schemas.BookOut, status_code=status.HTTP_201_CREATED)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db), current_user_id: int = 1):
    author = db.query(models.User).filter(models.User.id == current_user_id).first()
    if not author:
        raise HTTPException(status_code=404, detail="نویسنده معتبر یافت نشد")

    new_book = models.Book(
        title=book.title,
        description=book.description,
        price=book.price,
        stock_quantity=book.stock_quantity,
        is_available=book.is_available,
        author_id=current_user_id
    )
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book

@router.get("/", response_model=List[schemas.BookOut])
def get_books(db: Session = Depends(get_db)):
    return db.query(models.Book).all()