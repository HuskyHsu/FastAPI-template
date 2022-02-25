from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.post("", response_model=schemas.UserResponse, name="register")
def create_user(user_in: schemas.UserCreate, db: Session = Depends(deps.get_db)) -> Any:
    user = crud.user.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(status_code=400, detail="Email already registered")
    user = crud.user.create_user(db=db, obj_in=user_in)
    # TODO: send_new_account_email
    return schemas.UserResponse.from_orm(user)


@router.get("", response_model=list[schemas.UserResponse])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(deps.get_db),
               current_user: models.User = Depends(deps.get_current_active_user)):
    if not current_user.is_superuser:
        raise HTTPException(status_code=401, detail="Unauthorized")

    users = crud.user.get_multi(db, skip=skip, limit=limit)
    return [schemas.UserResponse.from_orm(user) for user in users]


@router.get("/me", response_model=schemas.UserResponse)
def read_user_me(
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get current user.
    """
    return schemas.UserResponse.from_orm(current_user)


@router.put("/me", response_model=schemas.UserResponse)
def update_user_me(
    *,
    db: Session = Depends(deps.get_db),
    user_update: schemas.UserUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update own user.
    """
    current_user_data = jsonable_encoder(current_user)

    user_in = schemas.UserUpdate(**current_user_data)
    if user_update.password is not None:
        user_in.password = user_update.password
    if user_update.name is not None:
        user_in.name = user_update.name

    user = crud.user.update_user(db, user_id=current_user.id, obj_in=user_in)
    return schemas.UserResponse.from_orm(user)


@router.get("/{user_id}", response_model=schemas.UserResponse)
def read_user(user_id: int, db: Session = Depends(deps.get_db),
              current_user: models.User = Depends(deps.get_current_active_user)):
    if not current_user.is_superuser:
        raise HTTPException(status_code=401, detail="Unauthorized")

    user = crud.user.get(db, id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return schemas.UserResponse.from_orm(user)


# @router.post("/{user_id}/items", response_model=schemas.Item)
# def create_item_for_user(
#     user_id: int, item: schemas.ItemCreate, db: Session = Depends(deps.get_db)
# ):
#     return crud.user.create_item(db=db, item=item, user_id=user_id)
