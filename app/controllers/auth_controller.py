from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.auth_service import AuthService
from app.services.user_service import UserService
from app.views.user_schemas import (
    UserCreate, UserLogin, OTPVerify, OTPRequest,
    TokenResponse, UserResponse
)
from app.dependencies.auth_deps import get_current_user
from app.models.user_model import User

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    """ثبت نام کاربر جدید"""
    user_service = UserService(db)
    try:
        user = user_service.create_user(
            username=user_data.username,
            email=user_data.email,
            password=user_data.password,
            full_name=user_data.full_name
        )
        return user
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.post("/login", response_model=TokenResponse)
async def login(
    login_data: UserLogin,
    db: Session = Depends(get_db)
):
    """مرحله اول ورود: بررسی پسورد و ارسال OTP"""
    auth_service = AuthService(db)
    success, message, otp_code = auth_service.login_with_password(
        login_data.username,
        login_data.password
    )
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=message
        )
    
    return TokenResponse(
        access_token="",  # توکن بعد از تایید OTP صادر می‌شود
        user=UserResponse.from_orm(auth_service.user_service.get_by_username(login_data.username)),
        requires_otp=True
    )

@router.post("/verify-otp", response_model=TokenResponse)
async def verify_otp(
    otp_data: OTPVerify,
    db: Session = Depends(get_db)
):
    """مرحله دوم ورود: تایید OTP و دریافت توکن"""
    auth_service = AuthService(db)
    success, token, user = auth_service.verify_otp_and_login(
        otp_data.email,
        otp_data.otp_code
    )
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=token  # پیام خطا
        )
    
    return TokenResponse(
        access_token=token,
        user=UserResponse.from_orm(user),
        requires_otp=False
    )

@router.post("/resend-otp", response_model=dict)
async def resend_otp(
    otp_data: OTPRequest,
    db: Session = Depends(get_db)
):
    """درخواست OTP جدید"""
    auth_service = AuthService(db)
    success, otp_code = auth_service.request_new_otp(otp_data.email)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=otp_code
        )
    
    return {
        "message": "OTP sent successfully",
        "otp_code": otp_code  # فقط برای تست
    }

@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: User = Depends(get_current_user)
):
    """دریافت اطلاعات کاربر جاری"""
    return current_user