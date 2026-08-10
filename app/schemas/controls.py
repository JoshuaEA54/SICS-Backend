from pydantic import BaseModel, ConfigDict, Field

from app.core.enums import ControlCriticality


# ── Control Groups ────────────────────────────────────────────────────────────

class ControlGroupCreate(BaseModel):
    id: str = Field(max_length=10)  # Ej: "G01" — se provee manualmente
    name: str = Field(max_length=200)
    description: str | None = Field(default=None, max_length=1000)
    criticality: ControlCriticality = ControlCriticality.low


class ControlGroupUpdate(BaseModel):
    name: str = Field(max_length=200)
    description: str | None = Field(default=None, max_length=1000)
    criticality: ControlCriticality = ControlCriticality.low


class ControlGroupRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    name: str
    description: str | None
    criticality: ControlCriticality


# ── Controls ──────────────────────────────────────────────────────────────────

class ControlCreate(BaseModel):
    id: str  # Ej: "CC-GOV-01" — se provee manualmente
    group_id: str
    name: str
    description: str | None = None


class ControlUpdate(BaseModel):
    group_id: str
    name: str
    description: str | None = None


class ControlRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    group_id: str
    name: str
    description: str | None


# ── Standards ─────────────────────────────────────────────────────────────────

class StandardCreate(BaseModel):
    name: str  # Ej: "ISO27001", "NIST_CSF"


class StandardUpdate(BaseModel):
    name: str


class StandardRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str


# ── Control Standard Refs ─────────────────────────────────────────────────────

class ControlStandardRefCreate(BaseModel):
    control_id: str
    standard_id: int
    ref_code: str  # Ej: "5.2", "A.5.1.1", "ID.GV-1"


class ControlStandardRefRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    control_id: str
    standard_id: int
    ref_code: str


# ── Questionnaire (nested read) ───────────────────────────────────────────────

class StandardRefNested(BaseModel):
    standard_name: str
    clause: str


class ControlNested(BaseModel):
    id: str
    name: str
    description: str | None
    standards: list[StandardRefNested]


class ControlGroupFull(BaseModel):
    id: str
    name: str
    description: str | None
    controls: list[ControlNested]
