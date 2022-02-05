from typing import Optional
from sqlalchemy.orm import Session

from app import schemas
from app.models.item import Item
from app.crud.base import CRUDBase
from app.schemas.item import ItemCreate, ItemUpdate


class CRUDItem(CRUDBase[Item, ItemCreate, ItemUpdate]):
    pass


item = CRUDItem(Item)
