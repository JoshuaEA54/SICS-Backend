import shutil
import uuid
from pathlib import Path

from fastapi import UploadFile
from sqlalchemy.orm import Session

from app import crud
from app.core.config import settings
from app.core.exceptions import FileUploadError
from app.models.evaluation import Evidence


def upload_evidence(
    db: Session,
    response_id: uuid.UUID,
    file: UploadFile,
) -> Evidence:
    dest = Path(settings.UPLOAD_FOLDER) / str(response_id) / file.filename
    evidence = crud.evaluation.stage_evidence(
        db,
        response_id=response_id,
        file_path=str(dest),
        file_name=file.filename,
        file_type=file.content_type,
    )
    try:
        dest.parent.mkdir(parents=True, exist_ok=True)
        with dest.open("wb") as f:
            shutil.copyfileobj(file.file, f)
    except OSError:
        db.rollback()
        raise FileUploadError("No se pudo guardar el archivo")
    db.commit()
    db.refresh(evidence)
    return evidence
