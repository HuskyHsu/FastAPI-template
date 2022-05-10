from typing import Optional
from pydantic import BaseModel, EmailStr
import uuid
from fastapi_users import schemas


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


class UserRead(schemas.BaseUser[uuid.UUID]):
    pass


class UserCreate(schemas.BaseUserCreate):
    pass


class UserUpdate(schemas.BaseUserUpdate):
    pass
