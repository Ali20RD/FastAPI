# # app/routers/user_router.py
# from fastapi import APIRouter, Depends, HTTPException, status
# from sqlalchemy.orm import Session
# from typing import List
# from app import models, schemas
# from app.database import get_db

# router = APIRouter(
#     prefix="/users",
#     tags=["Users"]
# )

# @router.post("/", response_model=schemas.UserOut, status_code=status.HTTP_201_CREATED)
# def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
#     # بررسی تکراری نبودن ایمیل
#     existing_user = db.query(models.User).filter(models.User.email == user.email).first()
#     if existing_user:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST, 
#             detail="کاربری با این ایمیل قبلاً ثبت‌نام کرده است"
#         )
    
#     # در دنیای واقعی رمز عبور باید هش شود (مثلا با bcrypt)
#     # اما در حال حاضر آن را ساده ذخیره می‌کنیم تا سیستم احراز هویت تکمیل شود
#     new_user = models.User(
#         username=user.username,
#         email=user.email,
#         password=user.password,  # رمز عبور خام
#         role="user"  # نقش پیش‌فرض برای کاربران جدید
#     )
    
#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)
#     return new_user

# @router.get("/", response_model=List[schemas.UserOut])
# def get_users(db: Session = Depends(get_db)):
#     users = db.query(models.User).all()
#     return users

# @router.get("/{user_id}", response_model=schemas.UserOut)
# def get_user(user_id: int, db: Session = Depends(get_db)):
#     user = db.query(models.User).filter(models.User.id == user_id).first()
#     if not user:
#         raise HTTPException(status_code=404, detail="کاربر مورد نظر یافت نشد")
#     return user

# @router.patch("/{user_id}", response_model=schemas.UserOut)
# def update_user(user_id: int, update_data: schemas.UserUpdate, db: Session = Depends(get_db)):
#     user = db.query(models.User).filter(models.User.id == user_id).first()
#     if not user:
#         raise HTTPException(status_code=404, detail="کاربر مورد نظر یافت نشد")

#     if update_data.username is not None:
#         user.username = update_data.username
#     if update_data.email is not None:
#         user.email = update_data.email
#     if update_data.password is not None:
#         user.password = update_data.password
#     if update_data.role is not None:
#         user.role = update_data.role

#     db.commit()
#     db.refresh(user)
#     return user

# @router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
# def delete_user(user_id: int, db: Session = Depends(get_db)):
#     user = db.query(models.User).filter(models.User.id == user_id).first()
#     if not user:
#         raise HTTPException(status_code=404, detail="کاربر مورد نظر یافت نشد")

#     db.delete(user)
#     db.commit()
#     return



# app/routers/user_router.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app import models, schemas  # به راحتی از پکیج اصلی ایمپورت می‌کنیم
from app.database import get_db

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=schemas.UserOut, status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="کاربری با این ایمیل قبلاً ثبت‌نام کرده است")
    
    new_user = models.User(
        username=user.username,
        email=user.email,
        password=user.password,
        role="user"
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/", response_model=List[schemas.UserOut])
def get_users(db: Session = Depends(get_db)):
    return db.query(models.User).all()