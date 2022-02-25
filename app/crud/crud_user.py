from typing import Any, Dict, Optional, Union

from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from sqlalchemy import select

# from app import schemas
from app.core.security import get_password_hash, verify_password
# from app.models.item import Item
from app.models.user import User
from app.crud.base import CRUDBase
from app.schemas.user import UserCreate, UserUpdate


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def get_by_email(self, db: Session, *, email: str) -> Optional[User]:
        stmt = select(User).where(User.email == email).slice(0, 1)
        user = db.execute(stmt).first()
        return None if user is None else user[0]

    def create_user(self, db: Session, *, obj_in: UserCreate) -> User:
        db_obj = User(
            name=obj_in.name,
            email=obj_in.email,
            hashed_password=get_password_hash(obj_in.password),
            is_active=True
        )
        user_id = self.create(db, obj_in=db_obj)
        user = self.get(db, user_id)
        return user

    def update_user(
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

        self.update(db, id=user_id, obj_in=update_data)
        user = self.get(db, user_id)
        return user

    def update_last_login(
        self, db: Session, db_obj: User
    ) -> User:
        db_obj.last_login = func.now()
        return db.commit()

    def authenticate(self, db: Session, *, email: str, password: str) -> Optional[User]:
        user = self.get_by_email(db, email=email)

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
