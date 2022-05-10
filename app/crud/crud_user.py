from typing import Any, Dict, Optional, Union

from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from sqlalchemy import select
from app.config import Setting

# from app import schemas
from app.core.security import get_password_hash, verify_password

# from app.models.item import Item
from app.models.user import User
from app.crud.base import CRUDBase
from app.schemas.user import UserCreate, UserUpdate

import uuid
from typing import Optional

from fastapi import Depends, Request
from fastapi_users import BaseUserManager, FastAPIUsers, UUIDIDMixin
from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
    JWTStrategy,
)
from fastapi_users.db import SQLAlchemyUserDatabase

from app.db import User, get_user_db

SECRET = Setting.SECRET_KEY


class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        print(f"User {user.id} has registered.")

    async def on_after_forgot_password(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        print(f"User {user.id} has forgot their password. Reset token: {token}")

    async def on_after_request_verify(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        print(f"Verification requested for user {user.id}. Verification token: {token}")


async def get_user_manager(user_db: SQLAlchemyUserDatabase = Depends(get_user_db)):
    yield UserManager(user_db)


bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[User, uuid.UUID](get_user_manager, [auth_backend])

current_active_user = fastapi_users.current_user(active=True)


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    async def get_by_email(self, db: Session, *, email: str) -> Optional[User]:
        stmt = select(User).where(User.email == email).slice(0, 1)
        result = await db.execute(stmt)
        user = result.first()
        return None if user is None else user[0]

    async def create_user(self, db: Session, *, obj_in: UserCreate) -> User:
        db_obj = User(
            name=obj_in.name,
            email=obj_in.email,
            hashed_password=get_password_hash(obj_in.password),
            is_active=True,
        )
        user_id = await self.create(db, obj_in=db_obj)
        user = await self.get(db, user_id)
        return user

    async def update_user(
        self, db: Session, *, user_id: int, obj_in: Union[UserUpdate, Dict[str, Any]]
    ) -> User:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)

        if update_data["password"]:
            hashed_password = get_password_hash(update_data["password"])
            del update_data["password"]
            update_data["hashed_password"] = hashed_password

        await self.update(db, id=user_id, obj_in=update_data)
        user = await self.get(db, id=user_id)
        return user

    async def update_last_login(self, db: Session, db_obj: User) -> User:
        db_obj.last_login = func.now()
        return await db.commit()

    async def authenticate(
        self, db: Session, *, email: str, password: str
    ) -> Optional[User]:
        user = await self.get_by_email(db, email=email)

        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    def is_active(self, user: User) -> bool:
        return user.is_active

    def is_superuser(self, user: User) -> bool:
        return user.is_superuser


user = CRUDUser(User)
