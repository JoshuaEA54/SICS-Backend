import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr

from app.core.enums import UserRole


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    job_title: str | None = None
    role: UserRole
    company_id: uuid.UUID | None = None


class UserUpdate(BaseModel):
    name: str | None = None
    job_title: str | None = None
    role: UserRole | None = None
    company_id: uuid.UUID | None = None


class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str
    email: EmailStr
    job_title: str | None
    role: UserRole
    company_id: uuid.UUID | None
    created_at: datetime
