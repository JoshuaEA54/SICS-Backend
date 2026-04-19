from fastapi import APIRouter, Depends
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session

from app import crud
from app.api.deps import get_db
from app.schemas.geography import CantonRead, DistrictRead, ProvinceRead

router = APIRouter(prefix="/geography", tags=["geography"])


@router.get("/provinces", response_model=Page[ProvinceRead])
def list_provinces(db: Session = Depends(get_db)):
    return paginate(db, crud.geography.get_provinces_query())


@router.get("/provinces/{province_id}/cantons", response_model=Page[CantonRead])
def list_cantons(province_id: int, db: Session = Depends(get_db)):
    return paginate(db, crud.geography.get_cantons_query(province_id))


@router.get("/cantons/{canton_id}/districts", response_model=Page[DistrictRead])
def list_districts(canton_id: int, db: Session = Depends(get_db)):
    return paginate(db, crud.geography.get_districts_query(canton_id))
