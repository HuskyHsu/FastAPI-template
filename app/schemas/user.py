from typing import Optional
from pydantic import BaseModel, EmailStr

# from app.schemas.item import Item


class UserInLogin(BaseModel):
    email: EmailStr
    password: str


class UserCreate(UserInLogin):
    name: str


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    name: str

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None

    is_staff: bool = False
    is_active: Optional[bool] = True
    is_superuser: bool = False


class UserUpdate(UserBase):
    password: Optional[str] = None


class UserInDBBase(UserBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True


class User(UserInDBBase):
    pass


class UserInDB(UserInDBBase):
    hashed_password: str
