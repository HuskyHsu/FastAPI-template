from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
import logging

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import select, insert, update

from app.db.base_class import Base

logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).

        **Parameters**

        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model

    def get(self, db: Session, id: Any) -> Optional[ModelType]:
        stmt = select(self.model).where(self.model.id == id).slice(0, 1)
        row = db.execute(stmt).first()
        return row[0]

    def get_multi(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[ModelType]:
        stmt = select(self.model).order_by(self.model.id).slice(skip, limit)
        return [row[0] for row in db.execute(stmt).all()]

    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        stmt = insert(self.model).values(
            **obj_in_data)
        result = db.execute(stmt)
        db.commit()
        return result.inserted_primary_key[0]

    def update(
        self,
        db: Session,
        *,
        id: int,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)

        stmt = (
            update(self.model).where(self.model.id == id).
            values(**update_data)
        )
        result = db.execute(stmt)
        db.commit()
        return result

    def remove(self, db: Session, *, id: int) -> ModelType:
        obj = db.query(self.model).get(id)
        db.delete(obj)
        db.commit()
        return obj
