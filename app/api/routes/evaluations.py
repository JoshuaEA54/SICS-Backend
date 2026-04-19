import uuid
from http import HTTPStatus

from fastapi import APIRouter, Depends, File, UploadFile
from fastapi.responses import FileResponse
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session

from app import crud
from app.api.deps import get_current_user, get_db
from app.services import evaluation as evaluation_service
from app.schemas.evaluation import (
    EvaluationCreate,
    EvaluationRead,
    EvaluationStatusUpdate,
    EvidenceRead,
    ResponseRead,
    ResponseUpsert,
    ResponseVerdictUpdate,
)

router = APIRouter(prefix="/evaluations", tags=["evaluations"], dependencies=[Depends(get_current_user)])


# ── Evaluations ───────────────────────────────────────────────────────────────

@router.get("/", response_model=Page[EvaluationRead])
def list_evaluations(company_id: uuid.UUID | None = None, db: Session = Depends(get_db)):
    return paginate(db, crud.evaluation.get_evaluations_query(company_id))


@router.post("/", response_model=EvaluationRead, status_code=HTTPStatus.CREATED)
def create_evaluation(data: EvaluationCreate, db: Session = Depends(get_db)):
    return crud.evaluation.create_evaluation(db, data)


@router.get("/{eval_id}", response_model=EvaluationRead)
def get_evaluation(eval_id: uuid.UUID, db: Session = Depends(get_db)):
    return crud.evaluation.get_evaluation(db, eval_id)


@router.patch("/{eval_id}/status", response_model=EvaluationRead)
def update_evaluation_status(eval_id: uuid.UUID, data: EvaluationStatusUpdate, db: Session = Depends(get_db)):
    return crud.evaluation.update_evaluation_status(db, eval_id, data)


# ── Responses ─────────────────────────────────────────────────────────────────

@router.get("/{eval_id}/responses", response_model=Page[ResponseRead])
def list_responses(eval_id: uuid.UUID, db: Session = Depends(get_db)):
    return paginate(db, crud.evaluation.get_responses_query(eval_id))


@router.put("/{eval_id}/responses", response_model=ResponseRead)
def upsert_response(eval_id: uuid.UUID, data: ResponseUpsert, db: Session = Depends(get_db)):
    data.evaluation_id = eval_id
    return crud.evaluation.upsert_response(db, data)


@router.patch("/responses/{response_id}/verdict", response_model=ResponseRead)
def update_response_verdict(response_id: uuid.UUID, data: ResponseVerdictUpdate, db: Session = Depends(get_db)):
    return crud.evaluation.update_response_verdict(db, response_id, data)


# ── Evidence ──────────────────────────────────────────────────────────────────

@router.get("/responses/{response_id}/evidence", response_model=Page[EvidenceRead])
def list_evidence(response_id: uuid.UUID, db: Session = Depends(get_db)):
    return paginate(db, crud.evaluation.get_evidence_query(response_id))


@router.post("/responses/{response_id}/evidence", response_model=EvidenceRead, status_code=HTTPStatus.CREATED)
async def upload_evidence(
    response_id: uuid.UUID,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    return evaluation_service.upload_evidence(db, response_id, file)


@router.get("/evidence/{evidence_id}/file")
def download_evidence(evidence_id: uuid.UUID, db: Session = Depends(get_db)):
    path, file_name, file_type = evaluation_service.get_evidence_file(db, evidence_id)
    return FileResponse(path=path, filename=file_name, media_type=file_type)


@router.delete("/evidence/{evidence_id}", status_code=HTTPStatus.NO_CONTENT)
def delete_evidence(evidence_id: uuid.UUID, db: Session = Depends(get_db)):
    evaluation_service.delete_evidence(db, evidence_id)
