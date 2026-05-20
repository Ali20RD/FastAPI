# redis_config.py
import redis
import random

# اتصال به دیتابیس ردیس
redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

def generate_and_save_otp(username: str) -> str:
    # تولید یک کد ۶ رقمی تصادفی
    otp_code = str(random.randint(100000, 999999))
    
    # ذخیره کد در ردیس با کلیدی بر اساس نام کاربری (انقضا: ۱۲۰ ثانیه)
    redis_client.setex(f"otp:{username}", 120, otp_code)
    
    # نمایش کد در کنسول سرور (طبق خواسته شما)
    print("\n" + "="*40)
    print(f"[SMS/Email Simulation] OTP Code for {username}: {otp_code}")
    print("="*40 + "\n")
    
    return otp_code

def verify_otp(username: str, user_code: str) -> bool:
    saved_code = redis_client.get(f"otp:{username}")
    if saved_code and saved_code == user_code:
        redis_client.delete(f"otp:{username}") # کد یکبار مصرف است، پس حذف می‌شود
        return True
    return False