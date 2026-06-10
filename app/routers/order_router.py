
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app import models, schemas
from app.database import get_db

router = APIRouter(prefix="/orders", tags=["Orders"])

@router.post("/", response_model=schemas.OrderOut, status_code=status.HTTP_201_CREATED)
def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db), current_user: int = 1):
    book = db.query(models.Book).filter(models.Book.id == order.book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    if book.stock_quantity < order.quantity:
        raise HTTPException(status_code=400, detail="The availability of books is not enough.")

    total_price = book.price * order.quantity

  
    new_order = models.Order(
        book_id=order.book_id,
        user_id=current_user,
        quantity=order.quantity,
        total_price=total_price,
    )

    book.stock_quantity -= order.quantity
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    return new_order

@router.get("/", response_model=List[schemas.OrderOut])
def get_orders(db: Session = Depends(get_db)):
    return db.query(models.Order).all()