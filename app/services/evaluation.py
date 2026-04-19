import uuid
from pathlib import Path

from fastapi import UploadFile
from sqlalchemy.orm import Session

from app import crud
from app.core.config import settings
from app.core.exceptions import FileUploadError, InvalidFileError
from app.models.evaluation import Evidence


def upload_evidence(
    db: Session,
    response_id: uuid.UUID,
    file: UploadFile,
) -> Evidence:
    if file.content_type not in settings.ALLOWED_MIME_TYPES:
        raise InvalidFileError("Tipo de archivo no permitido")

    safe_name = Path(file.filename).name
    if not safe_name or safe_name.startswith("."):
        raise InvalidFileError("Nombre de archivo inválido")

    max_bytes = settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024
    content = file.file.read(max_bytes + 1)
    if len(content) > max_bytes:
        raise InvalidFileError(f"El archivo supera el límite de {settings.MAX_UPLOAD_SIZE_MB} MB")

    dest = Path(settings.UPLOAD_FOLDER) / str(response_id) / safe_name
    evidence = crud.evaluation.stage_evidence(
        db,
        response_id=response_id,
        file_path=str(dest),
        file_name=safe_name,
        file_type=file.content_type,
    )
    try:
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(content)
    except OSError:
        db.rollback()
        raise FileUploadError("No se pudo guardar el archivo")
    db.commit()
    db.refresh(evidence)
    return evidence


def get_evidence_file(db: Session, evidence_id: uuid.UUID) -> tuple[Path, str, str | None]:
    evidence = crud.evaluation.get_evidence(db, evidence_id)
    path = Path(evidence.file_path)
    if not path.exists():
        raise FileUploadError("El archivo no se encuentra en el servidor")
    return path, evidence.file_name, evidence.file_type


def delete_evidence(db: Session, evidence_id: uuid.UUID) -> None:
    evidence = crud.evaluation.get_evidence(db, evidence_id)
    file_path = Path(evidence.file_path)

    crud.evaluation.delete_evidence(db, evidence_id)

    # best-effort: si el archivo ya no existe no es un error
    file_path.unlink(missing_ok=True)
