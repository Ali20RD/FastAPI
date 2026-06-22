from sqlalchemy import Column, Integer, String, DateTime, Boolean,ForeignKey, Enum
from datetime import datetime
from sqlalchemy import func
from app.models.base import BaseModel
from app.models.enums import UserRole

class User(BaseModel):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    # address = Column(integer, ForeignKey("address.id"))
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(100))
    role = Column(Enum(UserRole), default=UserRole.USER)
    is_verified = Column(Boolean, default=False)  # برای OTP
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now())
    
    # ============ سیستم مجوزها (RBAC) ============
    
    PERMISSIONS_MAP = {
        UserRole.ADMIN: {
            # مدیریت کاربران
            'user:create', 'user:read', 'user:update', 'user:delete',
            # مدیریت کتاب‌ها
            'book:create', 'book:read', 'book:update', 'book:delete',
            'book:update_any', 'book:delete_any',
            # مدیریت سفارشات
            'order:read', 'order:read_all', 'order:update', 'order:delete',
            # مدیریت موجودی
            'stock:update_any',
        },
        UserRole.AUTHOR: {
            # مدیریت کتاب‌های خود
            'book:create', 'book:read', 
            'book:update_own', 'book:delete_own',
            # موجودی کتاب‌های خود
            'stock:update_own',
            # مشاهده سفارشات خود
            'order:read_own',
        },
        UserRole.USER: {
            # مشاهده کتاب‌ها
            'book:read',
            # خرید کتاب
            'order:create', 'order:read_own',
        }
    }
    

    @staticmethod
    def get_permissions_for_role(role: UserRole) -> set:
        """دریافت مجوزهای یک نقش"""
        return User.PERMISSIONS_MAP.get(role, set())
    
    def has_permission(self, permission: str) -> bool:
        """بررسی دسترسی به یک مجوز خاص"""
        return permission in self.get_permissions_for_role(self.role)
    
    def has_any_permission(self, *permissions: str) -> bool:
        """بررسی دسترسی به حداقل یکی از مجوزها"""
        user_perms = self.get_permissions_for_role(self.role)
        return any(p in user_perms for p in permissions)
    
    def has_all_permissions(self, *permissions: str) -> bool:
        """بررسی دسترسی به همه مجوزها"""
        user_perms = self.get_permissions_for_role(self.role)
        return all(p in user_perms for p in permissions)
    
    def is_admin(self) -> bool:
        return self.role == UserRole.ADMIN
    
    def is_author(self) -> bool:
        return self.role == UserRole.AUTHOR
    
    def is_user(self) -> bool:
        return self.role == UserRole.USER
    
    @property
    def permissions(self) -> list:
        """لیست مجوزها (برای نمایش در API)"""
        return list(self.get_permissions_for_role(self.role))
    
    def __repr__(self):
        return f"<User {self.username} ({self.role.value})>"