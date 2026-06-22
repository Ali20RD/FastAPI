import random
import redis
from datetime import datetime, timedelta
from app.core.config import settings

# اتصال به Redis
redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)

class OTPService:
    
    @staticmethod
    def generate_otp() -> str:
        """تولید کد OTP 6 رقمی"""
        return ''.join([str(random.randint(0, 9)) for _ in range(6)])
    
    @staticmethod
    def get_otp_key(email: str) -> str:
        return f"otp:{email}"
    
    @staticmethod
    def send_otp(email: str) -> str:
        """ارسال OTP و ذخیره در Redis"""
        otp_code = OTPService.generate_otp()
        key = OTPService.get_otp_key(email)
        
        # ذخیره در Redis با انقضا
        redis_client.setex(
            key,
            timedelta(minutes=settings.OTP_EXPIRE_MINUTES),
            otp_code
        )
        
        # در محیط واقعی، ایمیل ارسال می‌شود
        # send_email(email, f"Your OTP code is: {otp_code}")
        
        # برای تست، کد را برمی‌گردانیم
        print(f"\n========================================\n[OTP SIMULATION] Code for {username}: {otp_code}\n========================================\n")
        return otp_code
    
    @staticmethod
    def verify_otp(email: str, otp_code: str) -> bool:
        """تایید OTP"""
        key = OTPService.get_otp_key(email)
        stored_otp = redis_client.get(key)
        
        if not stored_otp:
            return False
        
        if stored_otp != otp_code:
            return False
        
        # حذف OTP بعد از تایید
        redis_client.delete(key)
        return True
    
    @staticmethod
    def is_otp_valid(email: str) -> bool:
        """بررسی معتبر بودن OTP برای ایمیل"""
        key = OTPService.get_otp_key(email)
        return redis_client.exists(key) > 0





# import redis.asyncio as aioredis
# import random

# redis_client = aioredis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

# async def generate_and_save_otp(username: str) -> str:
#     otp_code = str(random.randint(100000, 999999))
#     await redis_client.setex(f"otp:{username}", 120, otp_code)
#     print(f"\n========================================\n[OTP SIMULATION] Code for {username}: {otp_code}\n========================================\n")
#     return otp_code

# async def verify_otp(username: str, user_code: str) -> bool:
#     saved_code = await redis_client.get(f"otp:{username}")
#     if saved_code and saved_code == user_code:
#         await redis_client.delete(f"otp:{username}")
#         return True
#     return False