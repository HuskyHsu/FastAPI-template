from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from fastapi_users.db import SQLAlchemyBaseUserTableUUID, SQLAlchemyUserDatabase

from app.db.base import Base


class User(SQLAlchemyBaseUserTableUUID, Base):
    __tablename__ = "users"
    name = Column(String(64))
    is_staff = Column(Boolean(), default=False)

    last_login = Column(DateTime(timezone=True), onupdate=func.now())
    date_joined = Column(DateTime(timezone=True), server_default=func.now())
