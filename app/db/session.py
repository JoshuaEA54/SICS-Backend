from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import settings


engine = create_engine(
	settings.sqlalchemy_database_uri,
	pool_pre_ping=True,
)

SessionLocal = sessionmaker(
	bind=engine,
	autoflush=False,
	autocommit=False,
	class_=Session,
)