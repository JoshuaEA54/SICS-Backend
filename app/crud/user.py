from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserCreate


def get_user_by_email(db: Session, email: str) -> User | None:
	statement = select(User).where(User.email == email)
	return db.execute(statement).scalar_one_or_none()


def create_user(db: Session, user_in: UserCreate) -> User:
	db_user = User(email=str(user_in.email), full_name=user_in.full_name)
	db.add(db_user)
	db.commit()
	db.refresh(db_user)
	return db_user