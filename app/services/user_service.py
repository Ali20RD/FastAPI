from typing import Optional, List
from sqlalchemy.orm import Session
from app.repositories.user_repository import UserRepository
from app.models.user_model import User
from app.models.enums import UserRole
from app.core.security import get_password_hash

class UserService:
    """سرویس مدیریت کاربران"""
    
    def __init__(self, db: Session):
        self.db = db
        self.repository = UserRepository(db)
    
    def create_user(self, username: str, email: str, password: str, 
                   full_name: str = None, role: UserRole = UserRole.USER) -> User:
        """ایجاد کاربر جدید"""
        # اعتبارسنجی
        if self.repository.get_by_username(username):
            raise ValueError("Username already exists")
        if self.repository.get_by_email(email):
            raise ValueError("Email already exists")
        
        # ایجاد کاربر
        return self.repository.create(
            username=username,
            email=email,
            hashed_password=get_password_hash(password),
            full_name=full_name,
            role=role,
            is_active=True
        )
    
    def get_by_id(self, user_id: int) -> Optional[User]:
        return self.repository.get_by_id(user_id)
    
    def get_by_username(self, username: str) -> Optional[User]:
        return self.repository.get_by_username(username)
    
    def get_by_email(self, email: str) -> Optional[User]:
        return self.repository.get_by_email(email)
    
    def get_all_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        return self.repository.get_all(skip, limit)
    
    def get_by_role(self, role: UserRole) -> List[User]:
        return self.repository.get_by_role(role)
    
    def update_user(self, user_id: int, **kwargs) -> Optional[User]:
        """بروزرسانی کاربر"""
        user = self.repository.get_by_id(user_id)
        if not user:
            return None
        
        # اگر پسورد تغییر کرده، هش می‌شود
        if 'password' in kwargs:
            kwargs['hashed_password'] = get_password_hash(kwargs.pop('password'))
        
        return self.repository.update(user_id, **kwargs)
    
    def update_role(self, user_id: int, new_role: UserRole) -> Optional[User]:
        """تغییر نقش کاربر"""
        user = self.repository.get_by_id(user_id)
        if not user:
            return None
        
        # نمی‌توان نقش ادمین را تغییر داد (برای امنیت)
        if user.is_admin() and new_role != UserRole.ADMIN:
            raise ValueError("Cannot change admin role")
        
        return self.repository.update_role(user_id, new_role)
    
    def delete_user(self, user_id: int) -> bool:
        """حذف کاربر"""
        user = self.repository.get_by_id(user_id)
        if not user:
            return False
        
        # نمی‌توان ادمین را حذف کرد
        if user.is_admin():
            raise ValueError("Cannot delete admin user")
        
        return self.repository.delete(user_id)
    
    def deactivate_user(self, user_id: int) -> Optional[User]:
        """غیرفعال کردن کاربر"""
        return self.repository.update(user_id, is_active=False)
    
    def activate_user(self, user_id: int) -> Optional[User]:
        """فعال کردن کاربر"""
        return self.repository.update(user_id, is_active=True)