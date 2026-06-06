import json
import uuid
from datetime import datetime, timezone

from sqlalchemy import Select, case, false, func, select
from sqlalchemy.orm import Session

from app.core.enums import EvaluationStatus
from app.core.exceptions import BadRequestError
from app.models.company import Company
from app.models.evaluation import Evaluation, Evidence, Response
from app.schemas.evaluation import (
    EvaluationCreate,
    EvaluationStatusUpdate,
    ResponseUpsert,
)


# ── Evaluation ────────────────────────────────────────────────────────────────

def get_evaluation(db: Session, eval_id: uuid.UUID) -> Evaluation:
    return db.execute(select(Evaluation).where(Evaluation.id == eval_id)).scalar_one()


def get_draft_evaluation(db: Session, company_id: uuid.UUID) -> Evaluation | None:
    return db.execute(
        select(Evaluation).where(
            Evaluation.company_id == company_id,
            Evaluation.status == EvaluationStatus.draft,
        ).limit(1)
    ).scalar_one_or_none()


def get_evaluations_query(
    company_id: uuid.UUID | None = None,
    status: EvaluationStatus | None = None,
    sector_id: int | None = None,
    exclude_draft: bool = False,
) -> Select:
    stmt = select(Evaluation)
    if sector_id is not None:
        stmt = stmt.join(Company, Company.id == Evaluation.company_id).where(
            Company.sector_id == sector_id
        )

    if exclude_draft:
        stmt = stmt.where(Evaluation.status != EvaluationStatus.draft)

    if company_id is not None:
        stmt = stmt.where(Evaluation.company_id == company_id)

    if status is not None:
        if exclude_draft and status == EvaluationStatus.draft:
            stmt = stmt.where(false())
        else:
            stmt = stmt.where(Evaluation.status == status)

    status_priority = case(
        (Evaluation.status == EvaluationStatus.submitted, 0),
        (Evaluation.status == EvaluationStatus.reviewed, 1),
        else_=2,
    )
    sort_date = case(
        (Evaluation.status == EvaluationStatus.reviewed, Evaluation.reviewed_at),
        else_=Evaluation.submitted_at,
    )
    stmt = stmt.order_by(
        status_priority.asc(),
        sort_date.desc().nulls_last(),
        Evaluation.created_at.desc(),
    )

    return stmt


def get_evaluation_status_counts(
    db: Session,
    company_id: uuid.UUID | None = None,
    exclude_draft: bool = False,
) -> dict[str, int]:
    def _count_for(status: EvaluationStatus) -> int:
        stmt = select(func.count()).select_from(Evaluation).where(Evaluation.status == status)
        if exclude_draft:
            stmt = stmt.where(Evaluation.status != EvaluationStatus.draft)
        if company_id is not None:
            stmt = stmt.where(Evaluation.company_id == company_id)
        return db.scalar(stmt) or 0

    return {
        "pending": _count_for(EvaluationStatus.submitted),
        "reviewed": _count_for(EvaluationStatus.reviewed),
    }


def create_evaluation(db: Session, data: EvaluationCreate) -> Evaluation:
    evaluation = Evaluation(company_id=data.company_id)
    db.add(evaluation)
    db.commit()
    db.refresh(evaluation)
    return evaluation


def update_last_group(db: Session, eval_id: uuid.UUID, last_group_id: str) -> Evaluation:
    evaluation = db.execute(select(Evaluation).where(Evaluation.id == eval_id)).scalar_one()
    evaluation.last_group_id = last_group_id
    db.commit()
    db.refresh(evaluation)
    return evaluation


def mark_report_email_sent(
    db: Session,
    eval_id: uuid.UUID,
    *,
    sent_at: datetime,
    sent_to: list[str],
) -> Evaluation:
    evaluation = get_evaluation(db, eval_id)
    evaluation.report_email_sent_at = sent_at
    evaluation.report_email_sent_to = json.dumps(sorted(sent_to))
    db.commit()
    db.refresh(evaluation)
    return evaluation


def update_evaluation_status(db: Session, eval_id: uuid.UUID, data: EvaluationStatusUpdate) -> Evaluation:
    evaluation = db.execute(select(Evaluation).where(Evaluation.id == eval_id)).scalar_one()
    if data.status == EvaluationStatus.reviewed:
        raise BadRequestError("Use el endpoint de finalizar revisión para marcar como revisada")
    evaluation.status = data.status
    if data.status == EvaluationStatus.submitted:
        evaluation.submitted_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(evaluation)
    return evaluation


# ── Response ──────────────────────────────────────────────────────────────────

def get_responses_query(eval_id: uuid.UUID) -> Select:
    return select(Response).where(Response.evaluation_id == eval_id)


def get_response_by_id(db: Session, response_id: uuid.UUID) -> Response:
    return db.execute(select(Response).where(Response.id == response_id)).scalar_one()


def list_responses(db: Session, eval_id: uuid.UUID) -> list[Response]:
    return list(db.scalars(get_responses_query(eval_id)).all())


def get_response(db: Session, eval_id: uuid.UUID, control_id: str) -> Response | None:
    return db.execute(
        select(Response).where(Response.evaluation_id == eval_id, Response.control_id == control_id)
    ).scalar_one_or_none()


def upsert_response(db: Session, eval_id: uuid.UUID, data: ResponseUpsert) -> Response:
    response = get_response(db, eval_id, data.control_id)
    if response is None:
        response = Response(
            evaluation_id=eval_id,
            control_id=data.control_id,
            answer=data.answer,
            observations=data.observations,
        )
        db.add(response)
    else:
        response.answer = data.answer
        response.observations = data.observations
    db.commit()
    db.refresh(response)
    return response


# ── Evidence ──────────────────────────────────────────────────────────────────

def get_evidence_query(response_id: uuid.UUID) -> Select:
    return select(Evidence).where(Evidence.response_id == response_id)


def stage_evidence(
    db: Session,
    response_id: uuid.UUID,
    file_path: str,
    file_name: str,
    file_type: str | None,
) -> Evidence:
    evidence = Evidence(
        response_id=response_id,
        file_path=file_path,
        file_name=file_name,
        file_type=file_type,
    )
    db.add(evidence)
    db.flush()
    return evidence


def get_evidence(db: Session, evidence_id: uuid.UUID) -> Evidence:
    return db.execute(select(Evidence).where(Evidence.id == evidence_id)).scalar_one()


def delete_evidence(db: Session, evidence_id: uuid.UUID) -> None:
    evidence = get_evidence(db, evidence_id)
    db.delete(evidence)
    db.commit()
