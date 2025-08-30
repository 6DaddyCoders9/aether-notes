from pydantic import BaseModel, EmailStr
from datetime import datetime

# Shared properties
class UserBase(BaseModel):
    email: EmailStr
    
# Properties to receive via API on creation
class UserCreate(UserBase):
    pass

# Properties to return to client
class User(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
        
# Properties to return when an OTP is requested
class UserOTP(UserBase):
    otp: str | None = None
    
    class Config:
        from_attributes = True
        
# Properties to receive via API for OTP verification
class UserVerifyOTP(UserBase):
    otp: str

# Properties to return upon successful login (the session token)
class Token(BaseModel):
    access_token: str
    token_type: str