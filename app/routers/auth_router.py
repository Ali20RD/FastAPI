# auth_router.py
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from app.redis_config import generate_and_save_otp, verify_otp

router = APIRouter(prefix="/auth", tags=["Authentication"])

class LoginRequest(BaseModel):
    username: str
    password: str # در دنیای واقعی رمز عبور اینجا هش و تایید می‌شود

class OTPVerifyRequest(BaseModel):
    username: str
    code: str

@router.post("/login-step1")
def login_step_one(request: LoginRequest):
    # مرحله اول: تایید نام کاربری و رمز عبور (اینجا فرض را بر درست بودن می‌گذاریم)
    # ساخت و "ارسال" کد به کنسول
    generate_and_save_otp(request.username)
    return {"message": "کد تایید دو مرحله‌ای تولید شد. لطفاً کنسول سرور را چک کنید."}

@router.post("/login-step2")
def login_step_two(request: OTPVerifyRequest):
    # مرحله دوم: بررسی کد وارد شده توسط کاربر از طریق Redis
    if verify_otp(request.username, request.code):
        return {"message": "ورود با موفقیت انجام شد!", "token": "fake-jwt-token-here"}
    
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="کد تایید اشتباه است یا منقضی شده است"
    )