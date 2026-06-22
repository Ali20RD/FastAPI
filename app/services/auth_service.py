from typing import Optional, Tuple
from sqlalchemy.orm import Session
from app.services.user_service import UserService
from app.core.security import verify_password, create_access_token
from app.core.otp import OTPService
from app.models.user_model import User

class AuthService:
    """سرویس احراز هویت"""
    
    def __init__(self, db: Session):
        self.db = db
        self.user_service = UserService(db)
    
    def login_with_password(self, username: str, password: str) -> Tuple[bool, Optional[str], Optional[str]]:
        """
        مرحله اول ورود: بررسی پسورد و ارسال OTP
        بازگشت: (موفقیت, پیام, OTP_Code)
        """
        user = self.user_service.get_by_username(username)
        if not user:
            return False, "Invalid username or password", None
        
        if not user.is_active:
            return False, "User account is deactivated", None
        
        if not verify_password(password, user.hashed_password):
            return False, "Invalid username or password", None
        
        # ارسال OTP
        otp_code = OTPService.send_otp(user.email)
        
        return True, "OTP sent to your email", otp_code
    
    def verify_otp_and_login(self, email: str, otp_code: str) -> Tuple[bool, Optional[str], Optional[User]]:
        """
        مرحله دوم ورود: تایید OTP و ورود
        بازگشت: (موفقیت, توکن, کاربر)
        """
        # تایید OTP
        if not OTPService.verify_otp(email, otp_code):
            return False, "Invalid or expired OTP", None
        
        # دریافت کاربر
        user = self.user_service.get_by_email(email)
        if not user:
            return False, "User not found", None
        
        if not user.is_active:
            return False, "User account is deactivated", None
        
        # ایجاد توکن
        access_token = create_access_token(data={"sub": str(user.id)})
        
        return True, access_token, user
    
    def request_new_otp(self, email: str) -> Tuple[bool, Optional[str]]:
        """درخواست OTP جدید"""
        user = self.user_service.get_by_email(email)
        if not user:
            return False, "User not found"
        
        otp_code = OTPService.send_otp(email)
        return True, otp_code