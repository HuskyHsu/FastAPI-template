from typing import Optional
from sqlalchemy.orm import Session

from app import schemas
from app.models.item import Item
from app.models.user import User
from app.crud.base import CRUDBase
from app.schemas.user import UserCreate, UserUpdate


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):

    def get_by_email(self, db: Session, *, email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email).first()

    def create(self, db: Session, *, obj_in: UserCreate) -> User:
        db_obj = User(
            email=obj_in.email,
            hashed_password=obj_in.password + "notreallyhashed",
            is_active=True
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def create_item(self, db: Session, *, item: schemas.ItemCreate, user_id: int) -> User:
        print(item)
        db_item = Item(**item.dict(), owner_id=user_id)
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        return db_item


user = CRUDUser(User)
