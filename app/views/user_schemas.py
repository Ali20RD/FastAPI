# from pydantic import BaseModel, EmailStr
# from typing import Optional
# from datetime import datetime
# from app.models.enums import UserRole

# class UserBase(BaseModel):
#     username: str
#     email: EmailStr
#     role: UserRole = UserRole.USER

# class UserCreate(UserBase):
#     password: str

# class UserUpdate(BaseModel):
#     username: Optional[str] = None
#     email: Optional[EmailStr] = None
#     password: Optional[str] = None

# class UserOut(UserBase):
#     id: int
#     is_blocked: bool
#     created_at: datetime
    
#     class Config:
#         from_attributes = True



from typing import Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field
from app.models.enums import UserRole

# ===== Base =====
class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    full_name: Optional[str] = None
    role: UserRole = UserRole.USER

# ===== Create =====
class UserCreate(UserBase):

    password: str = Field(..., min_length=6)

# ===== Update =====
class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None

# ===== Role Update =====
class UserRoleUpdate(BaseModel):
    role: UserRole

# ===== Response =====
class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    full_name: Optional[str]
    role: UserRole
    is_active: bool
    created_at: datetime
    
    class Config:
        orm_mode = True

class UserWithPermissions(UserResponse):
    permissions: list[str]
    
    @classmethod
    def from_user(cls, user):
        return cls(
            id=user.id,
            username=user.username,
            email=user.email,
            full_name=user.full_name,
            role=user.role,
            is_active=user.is_active,
            created_at=user.created_at,
            permissions=user.permissions
        )

# ===== Login =====
class UserLogin(BaseModel):
    username: str
    password: str

class OTPVerify(BaseModel):
    email: EmailStr
    otp_code: str

class OTPRequest(BaseModel):
    email: EmailStr

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse
    requires_otp: bool = False