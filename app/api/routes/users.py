import uuid

from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from app import crud
from app.api.deps import get_db
from app.schemas.user import UserCreate, UserRead, UserUpdate

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", response_model=Page[UserRead])
def list_users(db: Session = Depends(get_db)):
    return paginate(db, crud.user.get_users_query())


@router.post("/", response_model=UserRead, status_code=201)
def create_user(data: UserCreate, db: Session = Depends(get_db)):
    return crud.user.create_user(db, data)


@router.get("/{user_id}", response_model=UserRead)
def get_user(user_id: uuid.UUID, db: Session = Depends(get_db)):
    user = crud.user.get_user(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/{user_id}", response_model=UserRead)
def update_user(user_id: uuid.UUID, data: UserUpdate, db: Session = Depends(get_db)):
    try:
        return crud.user.update_user(db, user_id, data)
    except NoResultFound:
        raise HTTPException(status_code=404, detail="User not found")


@router.delete("/{user_id}", status_code=204)
def delete_user(user_id: uuid.UUID, db: Session = Depends(get_db)):
    try:
        crud.user.delete_user(db, user_id)
    except NoResultFound:
        raise HTTPException(status_code=404, detail="User not found")
    return Response(status_code=204)
