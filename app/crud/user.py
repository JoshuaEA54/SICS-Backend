import uuid

from sqlalchemy import Select, select
from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate


def get_user(db: Session, user_id: uuid.UUID) -> User:
    return db.execute(select(User).where(User.id == user_id)).scalar_one()


def get_user_by_email(db: Session, email: str) -> User | None:
    return db.execute(select(User).where(User.email == email)).scalar_one_or_none()


def get_users_query() -> Select:
    return select(User).order_by(User.name)


def create_user(db: Session, data: UserCreate) -> User:
    user = User(
        name=data.name,
        email=str(data.email),
        job_title=data.job_title,
        role=data.role,
        company_id=data.company_id,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def update_user(db: Session, user_id: uuid.UUID, data: UserUpdate) -> User:
    user = db.execute(select(User).where(User.id == user_id)).scalar_one()
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(user, field, value)
    db.commit()
    db.refresh(user)
    return user


def delete_user(db: Session, user_id: uuid.UUID) -> None:
    user = db.execute(select(User).where(User.id == user_id)).scalar_one()
    db.delete(user)
    db.commit()
