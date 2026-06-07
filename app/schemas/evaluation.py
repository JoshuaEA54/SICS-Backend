import json
import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, ValidationInfo, field_validator

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
    report_email_sent_at: datetime | None = None
    report_email_sent_to: list[str] | None = None

    @field_validator("report_email_sent_to", mode="before")
    @classmethod
    def parse_report_email_sent_to(cls, value: object) -> list[str] | None:
        if isinstance(value, str):
            try:
                parsed = json.loads(value)
            except json.JSONDecodeError:
                return None
            if isinstance(parsed, list):
                return [str(item) for item in parsed]
            return None
        return value  # type: ignore[return-value]


class EvaluationStatusUpdate(BaseModel):
    status: EvaluationStatus


class EvaluationLastGroupUpdate(BaseModel):
    last_group_id: str


class EvaluationInboxSummary(BaseModel):
    pending: int
    reviewed: int


class ReportRecipientItem(BaseModel):
    email: str
    label: str


class ReportRecipientsResponse(BaseModel):
    recipients: list[ReportRecipientItem]


class SendReportResponse(BaseModel):
    sent_at: datetime
    sent_to: list[str]


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
    expert_observations: str | None = None
    reviewed_at: datetime | None


class ResponseVerdictUpdate(BaseModel):
    verdict: ResponseVerdict
    expert_observations: str | None = Field(default=None, max_length=500)

    @field_validator("expert_observations", mode="after")
    @classmethod
    def validate_expert_observations(
        cls, value: str | None, info: ValidationInfo
    ) -> str | None:
        verdict: ResponseVerdict = info.data["verdict"]
        has_obs = bool(value and value.strip())
        if verdict == ResponseVerdict.complies and has_obs:
            raise ValueError(
                "No se admiten observaciones del experto cuando el veredicto es Cumple"
            )
        if verdict != ResponseVerdict.complies and not has_obs:
            raise ValueError(
                "Las observaciones del experto son obligatorias para este veredicto"
            )
        return value


# ── Evidence ──────────────────────────────────────────────────────────────────

class EvidenceRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    response_id: uuid.UUID
    file_path: str
    file_name: str
    file_type: str | None
    created_at: datetime
