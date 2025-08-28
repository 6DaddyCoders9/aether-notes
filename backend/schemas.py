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
        orm_mode = True