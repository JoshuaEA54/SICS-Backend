import shutil
import uuid
from pathlib import Path

from fastapi import APIRouter, Depends, File, HTTPException, Response, UploadFile
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from app import crud
from app.api.deps import get_db
from app.core.config import settings
from app.schemas.evaluation import (
    EvaluationCreate,
    EvaluationRead,
    EvaluationStatusUpdate,
    EvidenceRead,
    ResponseRead,
    ResponseUpsert,
    ResponseVerdictUpdate,
)

router = APIRouter(prefix="/evaluations", tags=["evaluations"])


# ── Evaluations ───────────────────────────────────────────────────────────────

@router.get("/", response_model=Page[EvaluationRead])
def list_evaluations(company_id: uuid.UUID | None = None, db: Session = Depends(get_db)):
    return paginate(db, crud.evaluation.get_evaluations_query(company_id))


@router.post("/", response_model=EvaluationRead, status_code=201)
def create_evaluation(data: EvaluationCreate, db: Session = Depends(get_db)):
    return crud.evaluation.create_evaluation(db, data)


@router.get("/{eval_id}", response_model=EvaluationRead)
def get_evaluation(eval_id: uuid.UUID, db: Session = Depends(get_db)):
    evaluation = crud.evaluation.get_evaluation(db, eval_id)
    if evaluation is None:
        raise HTTPException(status_code=404, detail="Evaluation not found")
    return evaluation


@router.patch("/{eval_id}/status", response_model=EvaluationRead)
def update_evaluation_status(eval_id: uuid.UUID, data: EvaluationStatusUpdate, db: Session = Depends(get_db)):
    try:
        return crud.evaluation.update_evaluation_status(db, eval_id, data)
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Evaluation not found")


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
    try:
        return crud.evaluation.update_response_verdict(db, response_id, data)
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Response not found")


# ── Evidence ──────────────────────────────────────────────────────────────────

@router.get("/responses/{response_id}/evidence", response_model=Page[EvidenceRead])
def list_evidence(response_id: uuid.UUID, db: Session = Depends(get_db)):
    return paginate(db, crud.evaluation.get_evidence_query(response_id))


@router.post("/responses/{response_id}/evidence", response_model=EvidenceRead, status_code=201)
async def upload_evidence(
    response_id: uuid.UUID,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    upload_dir = Path(settings.UPLOAD_FOLDER) / str(response_id)
    upload_dir.mkdir(parents=True, exist_ok=True)
    dest = upload_dir / file.filename
    with dest.open("wb") as f:
        shutil.copyfileobj(file.file, f)
    return crud.evaluation.create_evidence(
        db,
        response_id=response_id,
        file_path=str(dest),
        file_name=file.filename,
        file_type=file.content_type,
    )


@router.delete("/evidence/{evidence_id}", status_code=204)
def delete_evidence(evidence_id: uuid.UUID, db: Session = Depends(get_db)):
    try:
        crud.evaluation.delete_evidence(db, evidence_id)
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Evidence not found")
    return Response(status_code=204)
