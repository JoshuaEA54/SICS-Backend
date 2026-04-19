import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.core.enums import EvaluationStatus, ResponseVerdict


# ── Evaluation ────────────────────────────────────────────────────────────────

class EvaluationCreate(BaseModel):
    company_id: uuid.UUID


class EvaluationRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    company_id: uuid.UUID
    status: EvaluationStatus
    last_group_id: str | None
    submitted_at: datetime | None
    reviewed_at: datetime | None
    created_at: datetime


class EvaluationStatusUpdate(BaseModel):
    status: EvaluationStatus


# ── Response ──────────────────────────────────────────────────────────────────

class ResponseUpsert(BaseModel):
    control_id: str
    answer: bool
    observations: str | None = None


class ResponseRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    evaluation_id: uuid.UUID
    control_id: str
    answer: bool
    observations: str | None
    answered_at: datetime
    verdict: ResponseVerdict | None
    reviewed_at: datetime | None


class ResponseVerdictUpdate(BaseModel):
    verdict: ResponseVerdict


# ── Evidence ──────────────────────────────────────────────────────────────────

class EvidenceRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    response_id: uuid.UUID
    file_path: str
    file_name: str
    file_type: str | None
    created_at: datetime
