from sqlalchemy import Enum as SAEnum, ForeignKey, Integer, SmallInteger, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.core.enums import ControlCriticality
from app.db.base import Base


class Sector(Base):
    __tablename__ = "sectors"

    id: Mapped[int] = mapped_column(SmallInteger, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)


class EmployeeRange(Base):
    __tablename__ = "employee_ranges"

    id: Mapped[int] = mapped_column(SmallInteger, primary_key=True, autoincrement=True)
    label: Mapped[str] = mapped_column(String(20), nullable=False, unique=True)


class ControlGroup(Base):
    __tablename__ = "control_groups"

    id: Mapped[str] = mapped_column(String(10), primary_key=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    criticality: Mapped[ControlCriticality | None] = mapped_column(SAEnum(ControlCriticality, native_enum=False, create_constraint=True, name="ck_control_groups_criticality"), nullable=True)


class Control(Base):
    __tablename__ = "controls"

    id: Mapped[str] = mapped_column(String(20), primary_key=True)
    group_id: Mapped[str] = mapped_column(String(10), ForeignKey("control_groups.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)


class Standard(Base):
    __tablename__ = "standards"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(20), nullable=False, unique=True)


class ControlStandardRef(Base):
    __tablename__ = "control_standard_refs"
    __table_args__ = (UniqueConstraint("control_id", "standard_id", "ref_code"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    control_id: Mapped[str] = mapped_column(String(20), ForeignKey("controls.id"), nullable=False)
    standard_id: Mapped[int] = mapped_column(Integer, ForeignKey("standards.id"), nullable=False)
    ref_code: Mapped[str] = mapped_column(String(50), nullable=False)
