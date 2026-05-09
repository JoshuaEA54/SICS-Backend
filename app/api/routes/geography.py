from fastapi import APIRouter, Depends, HTTPException
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


@router.get("/cantons/{canton_id}", response_model=CantonRead)
def get_canton(canton_id: int, db: Session = Depends(get_db)):
    canton = crud.geography.get_canton(db, canton_id)
    if canton is None:
        raise HTTPException(status_code=404)
    return canton


@router.get("/districts/{district_id}", response_model=DistrictRead)
def get_district(district_id: int, db: Session = Depends(get_db)):
    district = crud.geography.get_district(db, district_id)
    if district is None:
        raise HTTPException(status_code=404)
    return district
