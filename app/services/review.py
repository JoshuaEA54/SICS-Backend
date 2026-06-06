import uuid
from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app import crud
from app.core.enums import EvaluationStatus, ReportStatus, UserRole
from app.core.exceptions import BadRequestError
from app.models.evaluation import Evaluation, Response
from app.models.user import User
from app.schemas.evaluation import EvaluationRead, ResponseVerdictUpdate, ReviewProgress
from app.services import compliance
from app.services.evaluation_access import (
    get_evaluation_for_expert_finalize,
    get_response_for_expert_verdict,
)


def list_responses(db: Session, eval_id: uuid.UUID) -> list[Response]:
    return crud.evaluation.list_responses(db, eval_id)


def enrich_evaluation_read(
    db: Session,
    evaluation: Evaluation,
    *,
    current_user: User | None = None,
    company_labels: tuple[str | None, str | None] | None = None,
) -> EvaluationRead:
    if company_labels is None:
        company_labels = crud.company.get_company_display_labels(db, evaluation.company_id)
    company_name, sector_name = company_labels

    base = EvaluationRead.model_validate(evaluation)
    sent_to = base.report_email_sent_to
    report_error = base.report_error
    if current_user is not None and current_user.role == UserRole.company_rep:
        sent_to = None
        report_error = None

    base = base.model_copy(
        update={
            "company_name": company_name,
            "sector_name": sector_name,
            "report_email_sent_to": sent_to,
            "report_error": report_error,
        }
    )
    responses = list_responses(db, evaluation.id)

    if evaluation.status == EvaluationStatus.reviewed:
        compliant_count = sum(1 for r in responses if compliance.response_is_compliant(r))
        return base.model_copy(
            update={
                "compliance_percentage": compliance.calculate_compliance_percentage(responses),
                "compliant_count": compliant_count,
                "total_controls": len(responses),
            }
        )
    if evaluation.status == EvaluationStatus.submitted:
        completed, required = compliance.calculate_review_progress(responses)
        return base.model_copy(
            update={"review_progress": ReviewProgress(completed=completed, required=required)}
        )
    return base


def update_response_verdict(
    db: Session,
    response_id: uuid.UUID,
    data: ResponseVerdictUpdate,
) -> Response:
    response, _ = get_response_for_expert_verdict(db, response_id)

    if not response.answer:
        raise BadRequestError(
            "No se puede emitir veredicto cuando la empresa indicó que no cumple"
        )

    response.verdict = data.verdict
    response.expert_observations = data.expert_observations
    response.reviewed_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(response)
    return response


def finalize_review(db: Session, eval_id: uuid.UUID) -> Evaluation:
    evaluation = get_evaluation_for_expert_finalize(db, eval_id)

    responses = list_responses(db, eval_id)
    if compliance.has_pending_verdicts(responses):
        raise BadRequestError(
            "Faltan veredictos en controles donde la empresa indicó que cumple"
        )
    if compliance.has_missing_expert_observations(responses):
        raise BadRequestError(
            "Faltan observaciones del experto en controles con veredicto que las requiere"
        )

    evaluation.status = EvaluationStatus.reviewed
    evaluation.reviewed_at = datetime.now(timezone.utc)
    evaluation.report_status = ReportStatus.generating
    evaluation.report_error = None
    db.commit()
    db.refresh(evaluation)
    return evaluation
