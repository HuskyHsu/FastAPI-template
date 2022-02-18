from typing import Optional
from pydantic import BaseModel, EmailStr

# from app.schemas.item import Item


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    name: str
    password: str


class UserLogin(UserBase):
    password: str


class UserUpdate(BaseModel):
    name: str
    password: Optional[str]


class UserResponse(UserBase):
    id: int
    name: str

    class Config:
        orm_mode = True


class UserInDB(UserCreate):
    hashed_password: str

    is_staff: bool = False
    is_active: Optional[bool] = True
    is_superuser: bool = False


class User(UserCreate):
    pass
