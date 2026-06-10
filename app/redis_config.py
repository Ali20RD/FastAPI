# redis_config.py
import redis
import random

# Connecting to the Redis database
redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

def generate_and_save_otp(username: str) -> str:
    # Generate a random 6-digit code
    otp_code = str(random.randint(100000, 999999))
    
    # Store code in Redis with a key based on username (expires: 120 seconds)
    redis_client.setex(f"otp:{username}", 120, otp_code)
    
    # Show code in server console
    print("\n" + "="*40)
    print(f"[SMS/Email Simulation] OTP Code for {username}: {otp_code}")
    print("="*40 + "\n")
    
    return otp_code

def verify_otp(username: str, user_code: str) -> bool:
    saved_code = redis_client.get(f"otp:{username}")
    if saved_code and saved_code == user_code:
        redis_client.delete(f"otp:{username}") # The code is one-time use, so it will be deleted.
        return True
    return False