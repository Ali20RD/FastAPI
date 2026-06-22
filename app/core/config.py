from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "postgresql://user:pass@localhost:5432/bookstore"
    
    # Security
    SECRET_KEY: str = "aesrdtfy8645fg645gy645res321srufg"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()