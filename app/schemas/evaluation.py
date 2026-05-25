import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.core.enums import EvaluationStatus, ReportStatus, ResponseVerdict


# ── Evaluation ────────────────────────────────────────────────────────────────

class ReviewProgress(BaseModel):
    completed: int
    required: int


class EvaluationCreate(BaseModel):
    company_id: uuid.UUID


class EvaluationRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    company_id: uuid.UUID
    company_name: str | None = None
    sector_name: str | None = None
    status: EvaluationStatus
    last_group_id: str | None
    submitted_at: datetime | None
    reviewed_at: datetime | None
    created_at: datetime
    compliance_percentage: float | None = None
    compliant_count: int | None = None
    total_controls: int | None = None
    review_progress: ReviewProgress | None = None
    report_status: ReportStatus | None = None
    report_generated_at: datetime | None = None
    report_error: str | None = None


class EvaluationStatusUpdate(BaseModel):
    status: EvaluationStatus


class EvaluationLastGroupUpdate(BaseModel):
    last_group_id: str


class EvaluationInboxSummary(BaseModel):
    pending: int
    reviewed: int


# ── Response ──────────────────────────────────────────────────────────────────

class ResponseUpsert(BaseModel):
    control_id: str
    answer: bool
    observations: str | None = Field(default=None, max_length=500)


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
