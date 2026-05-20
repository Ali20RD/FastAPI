# from fastapi import APIRouter, Depends, HTTPException, status
# from sqlalchemy.orm import Session
# from typing import List
# from app import models, schemas
# from app.database import get_db




# router = APIRouter(
#     prefix="/orders",
#     tags=["Orders"]
#                     )


# @router.post("/", response_model=schemas.OrderOut, status_code=status.HTTP_201_CREATED)
# def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db), current_user: int = 1):
#     # فرض کردیم id کاربر فعلاً = 1 است (در عمل از login/token گرفته می‌شه)
#     book = db.query(models.Book).filter(models.Book.id == order.book_id).first()
#     if not book:
#         raise HTTPException(status_code=404, detail="Book not found")

#     if book.stock_quantity < order.quantity:
#         raise HTTPException(status_code=400, detail="Not enough stock")

#     total_price = book.price * order.quantity

#     new_order = models.Order(
#         book_id=order.book_id,
#         user_id=current_user,
#         quantity=order.quantity,
#         total_price=total_price,
#     )

#     # کم کردن موجودی کتاب
#     book.stock_quantity -= order.quantity

#     db.add(new_order)
#     db.commit()
#     db.refresh(new_order)
#     return new_order


# @router.get("/", response_model=List[schemas.OrderOut])
# def get_orders(db: Session = Depends(get_db)):
#     orders = db.query(models.Order).all()
#     return orders




# @router.get("/{order_id}", response_model=schemas.OrderOut)
# def get_order(order_id: int, db: Session = Depends(get_db)):
#     order = db.query(models.Order).filter(models.Order.id == order_id).first()
#     if not order:
#         raise HTTPException(status_code=404, detail="Order not found")
#     return order





# @router.patch("/{order_id}", response_model=schemas.OrderOut)
# def update_order(order_id: int, update_data: schemas.OrderUpdate, db: Session = Depends(get_db)):
#     order = db.query(models.Order).filter(models.Order.id == order_id).first()
#     if not order:
#         raise HTTPException(status_code=404, detail="Order not found")

#     if update_data.status:
#         order.status = update_data.status
#     if update_data.quantity:
#         order.quantity = update_data.quantity

#     db.commit()
#     db.refresh(order)
#     return order


# @router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
# def delete_order(order_id: int, db: Session = Depends(get_db)):
#     order = db.query(models.Order).filter(models.Order.id == order_id).first()
#     if not order:
#         raise HTTPException(status_code=404, detail="Order not found")

#     db.delete(order)
#     db.commit()
#     return












# app/routers/order_router.py
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
        raise HTTPException(status_code=404, detail="کتاب یافت نشد")

    if book.stock_quantity < order.quantity:
        raise HTTPException(status_code=400, detail="موجودی کتاب کافی نیست")

    total_price = book.price * order.quantity

    # توجه: اگر مدل سفارش (Order) را هنوز در models/__init__.py اضافه نکرده‌اید،
    # ممکن است خطای AttributeError بگیرید. مطمئن شوید مدل در دیتابیس ساخته شده است.
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