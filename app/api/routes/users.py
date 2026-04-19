import uuid
from http import HTTPStatus

from fastapi import APIRouter, Depends
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session

from app import crud
from app.api.deps import get_current_user, get_db
from app.schemas.user import UserCreate, UserRead, UserUpdate

router = APIRouter(prefix="/users", tags=["users"], dependencies=[Depends(get_current_user)])


@router.get("/", response_model=Page[UserRead])
def list_users(db: Session = Depends(get_db)):
    return paginate(db, crud.user.get_users_query())


@router.post("/", response_model=UserRead, status_code=HTTPStatus.CREATED)
def create_user(data: UserCreate, db: Session = Depends(get_db)):
    return crud.user.create_user(db, data)


@router.get("/{user_id}", response_model=UserRead)
def get_user(user_id: uuid.UUID, db: Session = Depends(get_db)):
    return crud.user.get_user(db, user_id)


@router.put("/{user_id}", response_model=UserRead)
def update_user(user_id: uuid.UUID, data: UserUpdate, db: Session = Depends(get_db)):
    return crud.user.update_user(db, user_id, data)


@router.delete("/{user_id}", status_code=HTTPStatus.NO_CONTENT)
def delete_user(user_id: uuid.UUID, db: Session = Depends(get_db)):
    crud.user.delete_user(db, user_id)
