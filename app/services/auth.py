from sqlalchemy.orm import Session

from app.core.enums import UserRole
from app.models.company import Company
from app.models.user import User
from app.schemas.auth import RegisterRequest


def register_new_company(db: Session, email: str, data: RegisterRequest) -> tuple[Company, User]:
    company = Company(
        name=data.company_name,
        sector_id=data.sector_id,
        employee_range_id=data.employee_range_id,
        district_id=data.district_id,
        branch_count=data.branch_count,
    )
    db.add(company)
    db.flush()  # get company.id before committing

    user = User(
        name=data.name,
        email=email,
        job_title=data.job_title,
        role=UserRole.company_rep,
        company_id=company.id,
    )
    db.add(user)
    db.commit()
    db.refresh(company)
    db.refresh(user)
    return company, user
