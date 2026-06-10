
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
        raise HTTPException(status_code=404, detail="Valid author not found")

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