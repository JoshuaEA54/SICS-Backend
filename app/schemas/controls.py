from pydantic import BaseModel, ConfigDict

from app.core.enums import ControlCriticality


# ── Control Groups ────────────────────────────────────────────────────────────

class ControlGroupCreate(BaseModel):
    id: str  # Ej: "G01" — se provee manualmente
    name: str
    description: str | None = None
    criticality: ControlCriticality | None = None


class ControlGroupUpdate(BaseModel):
    name: str
    description: str | None = None
    criticality: ControlCriticality | None = None


class ControlGroupRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    name: str
    description: str | None
    criticality: ControlCriticality | None


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
