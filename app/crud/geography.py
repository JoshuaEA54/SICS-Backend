from sqlalchemy import Select, select
from sqlalchemy.orm import Session

from app.models.geography import Canton, District, Province


def get_provinces_query() -> Select:
    return select(Province).order_by(Province.name)


def get_cantons_query(province_id: int) -> Select:
    return select(Canton).where(Canton.province_id == province_id).order_by(Canton.name)


def get_districts_query(canton_id: int) -> Select:
    return select(District).where(District.canton_id == canton_id).order_by(District.name)


# Para uso interno (sin paginación)
def get_province(db: Session, province_id: int) -> Province | None:
    return db.execute(select(Province).where(Province.id == province_id)).scalar_one_or_none()


def get_canton(db: Session, canton_id: int) -> Canton | None:
    return db.execute(select(Canton).where(Canton.id == canton_id)).scalar_one_or_none()
