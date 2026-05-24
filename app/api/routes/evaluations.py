import uuid
from http import HTTPStatus

from fastapi import APIRouter, Depends, File, UploadFile
from fastapi.responses import FileResponse
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session

from app import crud
from app.api.deps import get_current_user, get_db, require_company_rep, require_expert
from app.core.enums import EvaluationStatus, UserRole
from app.core.exceptions import BadRequestError, ForbiddenError
from app.models.user import User
from app.schemas.evaluation import (
    EvaluationCreate,
    EvaluationInboxSummary,
    EvaluationLastGroupUpdate,
    EvaluationRead,
    EvaluationStatusUpdate,
    EvidenceRead,
    ResponseRead,
    ResponseUpsert,
    ResponseVerdictUpdate,
)
from app.services import evaluation as evaluation_service
from app.services import review as review_service
from app.services.evaluation_access import (
    effective_company_id_for_user,
    get_evaluation_for_company_edit,
    get_evaluation_for_read,
    get_evidence_for_company_edit,
    get_evidence_with_access,
    get_response_for_company_edit,
    get_response_with_access,
)

router = APIRouter(prefix="/evaluations", tags=["evaluations"], dependencies=[Depends(get_current_user)])


# ── Evaluations ───────────────────────────────────────────────────────────────

@router.get("/", response_model=Page[EvaluationRead])
def list_evaluations(
    company_id: uuid.UUID | None = None,
    status: EvaluationStatus | None = None,
    sector_id: int | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    scoped_company_id = effective_company_id_for_user(current_user, company_id)
    exclude_draft = current_user.role == UserRole.expert
    page = paginate(
        db,
        crud.evaluation.get_evaluations_query(
            company_id=scoped_company_id,
            status=status,
            sector_id=sector_id,
            exclude_draft=exclude_draft,
        ),
    )
    labels_map = crud.company.get_company_display_labels_map(
        db, {item.company_id for item in page.items}
    )
    page.items = [
        review_service.enrich_evaluation_read(
            db,
            item,
            company_labels=labels_map.get(item.company_id),
        )
        for item in page.items
    ]
    return page


@router.get("/summary", response_model=EvaluationInboxSummary)
def get_evaluations_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    scoped_company_id = effective_company_id_for_user(current_user, None)
    exclude_draft = current_user.role == UserRole.expert
    return crud.evaluation.get_evaluation_status_counts(
        db,
        company_id=scoped_company_id,
        exclude_draft=exclude_draft,
    )


@router.post("/", response_model=EvaluationRead, status_code=HTTPStatus.CREATED)
def create_evaluation(
    data: EvaluationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_company_rep),
):
    if current_user.company_id != data.company_id:
        raise ForbiddenError("Solo puede crear evaluaciones para su empresa")
    return review_service.enrich_evaluation_read(db, crud.evaluation.create_evaluation(db, data))


@router.get("/draft", response_model=EvaluationRead | None)
def get_draft_evaluation(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_company_rep),
):
    if current_user.company_id is None:
        raise ForbiddenError("Usuario de empresa sin organización asociada")
    evaluation = crud.evaluation.get_draft_evaluation(db, current_user.company_id)
    if evaluation is None:
        return None
    return review_service.enrich_evaluation_read(db, evaluation)


@router.get("/{eval_id}", response_model=EvaluationRead)
def get_evaluation(
    eval_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return review_service.enrich_evaluation_read(
        db, get_evaluation_for_read(db, eval_id, current_user)
    )


@router.post("/{eval_id}/finalize-review", response_model=EvaluationRead)
def finalize_review(
    eval_id: uuid.UUID,
    db: Session = Depends(get_db),
    _expert: User = Depends(require_expert),
):
    return review_service.enrich_evaluation_read(db, review_service.finalize_review(db, eval_id))


@router.patch("/{eval_id}/status", response_model=EvaluationRead)
def update_evaluation_status(
    eval_id: uuid.UUID,
    data: EvaluationStatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_company_rep),
):
    get_evaluation_for_company_edit(db, eval_id, current_user)
    if data.status != EvaluationStatus.submitted:
        raise BadRequestError("Solo se puede enviar la evaluación desde borrador")
    return review_service.enrich_evaluation_read(
        db, crud.evaluation.update_evaluation_status(db, eval_id, data)
    )


@router.patch("/{eval_id}/last-group", response_model=EvaluationRead)
def update_last_group(
    eval_id: uuid.UUID,
    data: EvaluationLastGroupUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_company_rep),
):
    get_evaluation_for_company_edit(db, eval_id, current_user)
    return review_service.enrich_evaluation_read(
        db, crud.evaluation.update_last_group(db, eval_id, data.last_group_id)
    )


# ── Responses ─────────────────────────────────────────────────────────────────

@router.get("/{eval_id}/responses", response_model=Page[ResponseRead])
def list_responses(
    eval_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    get_evaluation_for_read(db, eval_id, current_user)
    return paginate(db, crud.evaluation.get_responses_query(eval_id))


@router.put("/{eval_id}/responses", response_model=ResponseRead)
def upsert_response(
    eval_id: uuid.UUID,
    data: ResponseUpsert,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_company_rep),
):
    get_evaluation_for_company_edit(db, eval_id, current_user)
    return crud.evaluation.upsert_response(db, eval_id, data)


@router.patch("/responses/{response_id}/verdict", response_model=ResponseRead)
def update_response_verdict(
    response_id: uuid.UUID,
    data: ResponseVerdictUpdate,
    db: Session = Depends(get_db),
    _expert: User = Depends(require_expert),
):
    return review_service.update_response_verdict(db, response_id, data)


# ── Evidence ──────────────────────────────────────────────────────────────────

@router.get("/responses/{response_id}/evidence", response_model=Page[EvidenceRead])
def list_evidence(
    response_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    get_response_with_access(db, response_id, current_user)
    return paginate(db, crud.evaluation.get_evidence_query(response_id))


@router.post("/responses/{response_id}/evidence", response_model=list[EvidenceRead], status_code=HTTPStatus.CREATED)
async def upload_evidence(
    response_id: uuid.UUID,
    files: list[UploadFile] = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_company_rep),
):
    get_response_for_company_edit(db, response_id, current_user)
    return evaluation_service.upload_evidence_batch(db, response_id, files)


@router.get("/evidence/{evidence_id}/file")
def download_evidence(
    evidence_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    get_evidence_with_access(db, evidence_id, current_user)
    path, file_name, file_type = evaluation_service.get_evidence_file(db, evidence_id)
    return FileResponse(path=path, filename=file_name, media_type=file_type)


@router.delete("/evidence/{evidence_id}", status_code=HTTPStatus.NO_CONTENT)
def delete_evidence(
    evidence_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_company_rep),
):
    get_evidence_for_company_edit(db, evidence_id, current_user)
    evaluation_service.delete_evidence(db, evidence_id)
