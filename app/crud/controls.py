from sqlalchemy import Select, select
from sqlalchemy.orm import Session

from app.models.controls import Control, ControlGroup, ControlStandardRef, Standard
from app.schemas.controls import (
    ControlCreate,
    ControlGroupCreate,
    ControlGroupUpdate,
    ControlStandardRefCreate,
    ControlUpdate,
    StandardCreate,
    StandardUpdate,
)


# ── ControlGroup ──────────────────────────────────────────────────────────────

def get_control_groups_query() -> Select:
    return select(ControlGroup).order_by(ControlGroup.id)


def get_control_group(db: Session, group_id: str) -> ControlGroup | None:
    return db.execute(select(ControlGroup).where(ControlGroup.id == group_id)).scalar_one_or_none()


def create_control_group(db: Session, data: ControlGroupCreate) -> ControlGroup:
    group = ControlGroup(
        id=data.id,
        name=data.name,
        description=data.description,
        criticality=data.criticality,
    )
    db.add(group)
    db.commit()
    db.refresh(group)
    return group


def update_control_group(db: Session, group_id: str, data: ControlGroupUpdate) -> ControlGroup:
    group = db.execute(select(ControlGroup).where(ControlGroup.id == group_id)).scalar_one()
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(group, field, value)
    db.commit()
    db.refresh(group)
    return group


def delete_control_group(db: Session, group_id: str) -> None:
    group = db.execute(select(ControlGroup).where(ControlGroup.id == group_id)).scalar_one()
    db.delete(group)
    db.commit()


# ── Control ───────────────────────────────────────────────────────────────────

def get_controls_query(group_id: str | None = None) -> Select:
    stmt = select(Control).order_by(Control.id)
    if group_id is not None:
        stmt = stmt.where(Control.group_id == group_id)
    return stmt


def get_control(db: Session, control_id: str) -> Control | None:
    return db.execute(select(Control).where(Control.id == control_id)).scalar_one_or_none()


def create_control(db: Session, data: ControlCreate) -> Control:
    control = Control(
        id=data.id,
        group_id=data.group_id,
        name=data.name,
        description=data.description,
    )
    db.add(control)
    db.commit()
    db.refresh(control)
    return control


def update_control(db: Session, control_id: str, data: ControlUpdate) -> Control:
    control = db.execute(select(Control).where(Control.id == control_id)).scalar_one()
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(control, field, value)
    db.commit()
    db.refresh(control)
    return control


def delete_control(db: Session, control_id: str) -> None:
    control = db.execute(select(Control).where(Control.id == control_id)).scalar_one()
    db.delete(control)
    db.commit()


# ── Standard ──────────────────────────────────────────────────────────────────

def get_standards_query() -> Select:
    return select(Standard).order_by(Standard.name)


def create_standard(db: Session, data: StandardCreate) -> Standard:
    standard = Standard(name=data.name)
    db.add(standard)
    db.commit()
    db.refresh(standard)
    return standard


def update_standard(db: Session, standard_id: int, data: StandardUpdate) -> Standard:
    standard = db.execute(select(Standard).where(Standard.id == standard_id)).scalar_one()
    standard.name = data.name
    db.commit()
    db.refresh(standard)
    return standard


def delete_standard(db: Session, standard_id: int) -> None:
    standard = db.execute(select(Standard).where(Standard.id == standard_id)).scalar_one()
    db.delete(standard)
    db.commit()


# ── ControlStandardRef ────────────────────────────────────────────────────────

def get_standard_refs_query(control_id: str) -> Select:
    return select(ControlStandardRef).where(ControlStandardRef.control_id == control_id)


def create_standard_ref(db: Session, data: ControlStandardRefCreate) -> ControlStandardRef:
    ref = ControlStandardRef(
        control_id=data.control_id,
        standard_id=data.standard_id,
        ref_code=data.ref_code,
    )
    db.add(ref)
    db.commit()
    db.refresh(ref)
    return ref


def delete_standard_ref(db: Session, ref_id: int) -> None:
    ref = db.execute(select(ControlStandardRef).where(ControlStandardRef.id == ref_id)).scalar_one()
    db.delete(ref)
    db.commit()
