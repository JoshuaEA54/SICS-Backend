import uuid

from sqlalchemy import Select, select
from sqlalchemy.orm import Session

from app.models.evaluation import Evaluation, Evidence, Response
from app.schemas.evaluation import (
    EvaluationCreate,
    EvaluationStatusUpdate,
    ResponseUpsert,
    ResponseVerdictUpdate,
)


# ── Evaluation ────────────────────────────────────────────────────────────────

def get_evaluation(db: Session, eval_id: uuid.UUID) -> Evaluation:
    return db.execute(select(Evaluation).where(Evaluation.id == eval_id)).scalar_one()


def get_evaluations_query(company_id: uuid.UUID | None = None) -> Select:
    stmt = select(Evaluation).order_by(Evaluation.created_at.desc())
    if company_id is not None:
        stmt = stmt.where(Evaluation.company_id == company_id)
    return stmt


def create_evaluation(db: Session, data: EvaluationCreate) -> Evaluation:
    evaluation = Evaluation(company_id=data.company_id)
    db.add(evaluation)
    db.commit()
    db.refresh(evaluation)
    return evaluation


def update_evaluation_status(db: Session, eval_id: uuid.UUID, data: EvaluationStatusUpdate) -> Evaluation:
    evaluation = db.execute(select(Evaluation).where(Evaluation.id == eval_id)).scalar_one()
    evaluation.status = data.status
    db.commit()
    db.refresh(evaluation)
    return evaluation


# ── Response ──────────────────────────────────────────────────────────────────

def get_responses_query(eval_id: uuid.UUID) -> Select:
    return select(Response).where(Response.evaluation_id == eval_id)


def get_response(db: Session, eval_id: uuid.UUID, control_id: str) -> Response | None:
    return db.execute(
        select(Response).where(Response.evaluation_id == eval_id, Response.control_id == control_id)
    ).scalar_one_or_none()


def upsert_response(db: Session, data: ResponseUpsert) -> Response:
    response = get_response(db, data.evaluation_id, data.control_id)
    if response is None:
        response = Response(
            evaluation_id=data.evaluation_id,
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


def update_response_verdict(db: Session, response_id: uuid.UUID, data: ResponseVerdictUpdate) -> Response:
    response = db.execute(select(Response).where(Response.id == response_id)).scalar_one()
    response.verdict = data.verdict
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
    db.flush()  # validates FK without committing
    return evidence


def delete_evidence(db: Session, evidence_id: uuid.UUID) -> None:
    evidence = db.execute(select(Evidence).where(Evidence.id == evidence_id)).scalar_one()
    db.delete(evidence)
    db.commit()
