from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(64), index=True)
    email = Column(String(128), unique=True, index=True, nullable=False)
    hashed_password = Column(Text, nullable=False)

    is_staff = Column(Boolean(), default=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean(), default=False)

    last_login = Column(DateTime(timezone=True), onupdate=func.now())
    date_joined = Column(DateTime(timezone=True), server_default=func.now())

    items = relationship("Item", back_populates="owner")
