from typing import Optional
from pydantic import BaseModel, EmailStr, ConfigDict

# Shared user properties
class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None
    is_active: Optional[bool] = True
    role: Optional[str] = "customer"

# Schema for User Signup / Registration
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: Optional[str] = None

# Schema for User Profile Response (NEVER returns password)
class UserResponse(UserBase):
    id: int

    model_config = ConfigDict(from_attributes=True)