from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr


class UserBase(BaseModel):
	email: EmailStr
	full_name: str | None = None


class UserCreate(UserBase):
	pass


class UserRead(UserBase):
	id: int
	is_active: bool
	created_at: datetime

	model_config = ConfigDict(from_attributes=True)