
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from app.redis_config import generate_and_save_otp, verify_otp

router = APIRouter(prefix="/auth", tags=["Authentication"])

class LoginRequest(BaseModel):
    username: str
    password: str

class OTPVerifyRequest(BaseModel):
    username: str
    code: str

@router.post("/login-step1")
def login_step_one(request: LoginRequest):
    
    generate_and_save_otp(request.username)
    return {"message": "A two-step verification code has been generated. Please check the server console."}

@router.post("/login-step2")
def login_step_two(request: OTPVerifyRequest):
    
    if verify_otp(request.username, request.code):
        return {"message": "Login successful.", "token": "fake-jwt-token-here"}
    
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail= "The verification code is incorrect or has expired"
    )