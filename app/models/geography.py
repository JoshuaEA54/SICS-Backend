from sqlalchemy import ForeignKey, SmallInteger, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Province(Base):
    __tablename__ = "provinces"

    id: Mapped[int] = mapped_column(SmallInteger, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(60), nullable=False, unique=True)


class Canton(Base):
    __tablename__ = "cantons"
    __table_args__ = (UniqueConstraint("name", "province_id"),)

    id: Mapped[int] = mapped_column(SmallInteger, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(80), nullable=False)
    province_id: Mapped[int] = mapped_column(SmallInteger, ForeignKey("provinces.id"), nullable=False)


class District(Base):
    __tablename__ = "districts"
    __table_args__ = (UniqueConstraint("name", "canton_id"),)

    id: Mapped[int] = mapped_column(SmallInteger, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(80), nullable=False)
    canton_id: Mapped[int] = mapped_column(SmallInteger, ForeignKey("cantons.id"), nullable=False)
