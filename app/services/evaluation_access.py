import uuid

from sqlalchemy.orm import Session

from app import crud
from app.core.enums import EvaluationStatus, UserRole
from app.core.exceptions import BadRequestError, ForbiddenError
from app.models.evaluation import Evaluation, Evidence, Response
from app.models.user import User


def assert_can_read_evaluation(user: User, evaluation: Evaluation) -> None:
    if user.role == UserRole.expert:
        return
    if user.role == UserRole.company_rep and user.company_id == evaluation.company_id:
        return
    raise ForbiddenError("No tiene acceso a esta evaluación")


def effective_company_id_for_user(user: User, company_id: uuid.UUID | None) -> uuid.UUID | None:
    if user.role == UserRole.expert:
        return company_id
    if user.role == UserRole.company_rep:
        if user.company_id is None:
            raise ForbiddenError("Usuario de empresa sin organización asociada")
        return user.company_id
    raise ForbiddenError("Rol de usuario no autorizado")


def assert_company_owns_evaluation(user: User, evaluation: Evaluation) -> None:
    if user.role != UserRole.company_rep or user.company_id != evaluation.company_id:
        raise ForbiddenError("No tiene acceso a esta evaluación")


def assert_evaluation_draft(evaluation: Evaluation) -> None:
    if evaluation.status != EvaluationStatus.draft:
        raise BadRequestError("Solo se pueden modificar evaluaciones en borrador")


def assert_evaluation_submitted(evaluation: Evaluation) -> None:
    if evaluation.status != EvaluationStatus.submitted:
        raise BadRequestError("La evaluación debe estar enviada para esta acción")


def get_evaluation_for_read(db: Session, eval_id: uuid.UUID, user: User) -> Evaluation:
    evaluation = crud.evaluation.get_evaluation(db, eval_id)
    assert_can_read_evaluation(user, evaluation)
    return evaluation


def get_response_with_access(
    db: Session, response_id: uuid.UUID, user: User
) -> tuple[Response, Evaluation]:
    response = crud.evaluation.get_response_by_id(db, response_id)
    evaluation = crud.evaluation.get_evaluation(db, response.evaluation_id)
    assert_can_read_evaluation(user, evaluation)
    return response, evaluation


def get_evidence_with_access(
    db: Session, evidence_id: uuid.UUID, user: User
) -> tuple[Evidence, Evaluation]:
    evidence = crud.evaluation.get_evidence(db, evidence_id)
    _, evaluation = get_response_with_access(db, evidence.response_id, user)
    return evidence, evaluation


def get_evaluation_for_company_edit(db: Session, eval_id: uuid.UUID, user: User) -> Evaluation:
    """Carga una evaluación editable por la empresa (propia y en borrador)."""
    evaluation = crud.evaluation.get_evaluation(db, eval_id)
    assert_company_owns_evaluation(user, evaluation)
    assert_evaluation_draft(evaluation)
    return evaluation


def get_response_for_company_edit(
    db: Session, response_id: uuid.UUID, user: User
) -> tuple[Response, Evaluation]:
    """Carga una respuesta cuya evaluación la empresa puede editar (borrador)."""
    response, evaluation = get_response_with_access(db, response_id, user)
    assert_company_owns_evaluation(user, evaluation)
    assert_evaluation_draft(evaluation)
    return response, evaluation


def get_evidence_for_company_edit(
    db: Session, evidence_id: uuid.UUID, user: User
) -> tuple[Evidence, Evaluation]:
    """Carga una evidencia cuya evaluación la empresa puede editar (borrador)."""
    evidence, evaluation = get_evidence_with_access(db, evidence_id, user)
    assert_company_owns_evaluation(user, evaluation)
    assert_evaluation_draft(evaluation)
    return evidence, evaluation


def get_response_for_expert_verdict(
    db: Session, response_id: uuid.UUID
) -> tuple[Response, Evaluation]:
    """Carga una respuesta de una evaluación enviada, lista para veredicto del experto."""
    response = crud.evaluation.get_response_by_id(db, response_id)
    evaluation = crud.evaluation.get_evaluation(db, response.evaluation_id)
    assert_evaluation_submitted(evaluation)
    return response, evaluation


def get_evaluation_for_expert_finalize(db: Session, eval_id: uuid.UUID) -> Evaluation:
    """Carga una evaluación enviada, lista para cerrar la revisión."""
    evaluation = crud.evaluation.get_evaluation(db, eval_id)
    assert_evaluation_submitted(evaluation)
    return evaluation
