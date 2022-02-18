from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.post("", response_model=schemas.User, name="register")
def create_user(user_in: schemas.UserCreate, db: Session = Depends(deps.get_db)) -> Any:
    user = crud.user.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(status_code=400, detail="Email already registered")
    user = crud.user.create(db=db, obj_in=user_in)
    # send_new_account_email
    return user


@router.get("/me", response_model=schemas.UserResponse)
def read_user_me(
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get current user.
    """
    return schemas.UserResponse.from_orm(current_user)


# @router.get("", response_model=list[schemas.User])
# def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(deps.get_db)):
#     users = crud.user.get_multi(db, skip=skip, limit=limit)
#     return users


# @router.get("/{user_id}", response_model=schemas.User)
# def read_user(user_id: int, db: Session = Depends(deps.get_db)):
#     db_user = crud.user.get(db, id=user_id)
#     if db_user is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     return db_user


# @router.post("/{user_id}/items", response_model=schemas.Item)
# def create_item_for_user(
#     user_id: int, item: schemas.ItemCreate, db: Session = Depends(deps.get_db)
# ):
#     return crud.user.create_item(db=db, item=item, user_id=user_id)
