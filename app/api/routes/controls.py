from http import HTTPStatus

from fastapi import APIRouter, Depends
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session

from app import crud
from app.api.deps import get_db
from app.schemas.controls import (
    ControlCreate,
    ControlGroupCreate,
    ControlGroupRead,
    ControlGroupUpdate,
    ControlRead,
    ControlStandardRefCreate,
    ControlStandardRefRead,
    ControlUpdate,
    StandardCreate,
    StandardRead,
    StandardUpdate,
)

router = APIRouter(prefix="/controls", tags=["controls"])


# ── Control Groups ────────────────────────────────────────────────────────────

@router.get("/groups", response_model=Page[ControlGroupRead])
def list_control_groups(db: Session = Depends(get_db)):
    return paginate(db, crud.controls.get_control_groups_query())


@router.post("/groups", response_model=ControlGroupRead, status_code=HTTPStatus.CREATED)
def create_control_group(data: ControlGroupCreate, db: Session = Depends(get_db)):
    return crud.controls.create_control_group(db, data)


@router.put("/groups/{group_id}", response_model=ControlGroupRead)
def update_control_group(group_id: str, data: ControlGroupUpdate, db: Session = Depends(get_db)):
    return crud.controls.update_control_group(db, group_id, data)


@router.delete("/groups/{group_id}", status_code=HTTPStatus.NO_CONTENT)
def delete_control_group(group_id: str, db: Session = Depends(get_db)):
    crud.controls.delete_control_group(db, group_id)


# ── Standards ─────────────────────────────────────────────────────────────────

@router.get("/standards", response_model=Page[StandardRead])
def list_standards(db: Session = Depends(get_db)):
    return paginate(db, crud.controls.get_standards_query())


@router.post("/standards", response_model=StandardRead, status_code=HTTPStatus.CREATED)
def create_standard(data: StandardCreate, db: Session = Depends(get_db)):
    return crud.controls.create_standard(db, data)


@router.put("/standards/{standard_id}", response_model=StandardRead)
def update_standard(standard_id: int, data: StandardUpdate, db: Session = Depends(get_db)):
    return crud.controls.update_standard(db, standard_id, data)


@router.delete("/standards/{standard_id}", status_code=HTTPStatus.NO_CONTENT)
def delete_standard(standard_id: int, db: Session = Depends(get_db)):
    crud.controls.delete_standard(db, standard_id)


# ── Standard Refs ─────────────────────────────────────────────────────────────

@router.get("/{control_id}/standard-refs", response_model=Page[ControlStandardRefRead])
def list_standard_refs(control_id: str, db: Session = Depends(get_db)):
    return paginate(db, crud.controls.get_standard_refs_query(control_id))


@router.post("/standard-refs", response_model=ControlStandardRefRead, status_code=HTTPStatus.CREATED)
def create_standard_ref(data: ControlStandardRefCreate, db: Session = Depends(get_db)):
    return crud.controls.create_standard_ref(db, data)


@router.delete("/standard-refs/{ref_id}", status_code=HTTPStatus.NO_CONTENT)
def delete_standard_ref(ref_id: int, db: Session = Depends(get_db)):
    crud.controls.delete_standard_ref(db, ref_id)


# ── Controls ──────────────────────────────────────────────────────────────────

@router.get("/", response_model=Page[ControlRead])
def list_controls(group_id: str | None = None, db: Session = Depends(get_db)):
    return paginate(db, crud.controls.get_controls_query(group_id))


@router.post("/", response_model=ControlRead, status_code=HTTPStatus.CREATED)
def create_control(data: ControlCreate, db: Session = Depends(get_db)):
    return crud.controls.create_control(db, data)


@router.get("/{control_id}", response_model=ControlRead)
def get_control(control_id: str, db: Session = Depends(get_db)):
    return crud.controls.get_control(db, control_id)


@router.put("/{control_id}", response_model=ControlRead)
def update_control(control_id: str, data: ControlUpdate, db: Session = Depends(get_db)):
    return crud.controls.update_control(db, control_id, data)


@router.delete("/{control_id}", status_code=HTTPStatus.NO_CONTENT)
def delete_control(control_id: str, db: Session = Depends(get_db)):
    crud.controls.delete_control(db, control_id)
