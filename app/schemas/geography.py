from pydantic import BaseModel, ConfigDict


class ProvinceRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str


class CantonRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    province_id: int


class DistrictRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    canton_id: int
