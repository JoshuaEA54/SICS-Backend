import uuid
from pathlib import Path

from fastapi import UploadFile
from sqlalchemy.orm import Session

from app import crud
from app.core.config import settings
from app.core.exceptions import FileUploadError, InvalidFileError
from app.models.evaluation import Evidence


def upload_evidence_batch(
    db: Session,
    response_id: uuid.UUID,
    files: list[UploadFile],
) -> list[Evidence]:
    max_bytes = settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024
    prepared: list[tuple[str, str | None, bytes, Path]] = []
    for file in files:
        if file.content_type not in settings.ALLOWED_MIME_TYPES:
            raise InvalidFileError(f"Tipo de archivo no permitido: {file.filename}")
        safe_name = Path(file.filename).name
        if not safe_name or safe_name.startswith("."):
            raise InvalidFileError(f"Nombre de archivo inválido: {file.filename}")
        content = file.file.read(max_bytes + 1)
        if len(content) > max_bytes:
            raise InvalidFileError(f"El archivo '{safe_name}' supera el límite de {settings.MAX_UPLOAD_SIZE_MB} MB")
        dest = Path(settings.UPLOAD_FOLDER) / str(response_id) / safe_name
        prepared.append((safe_name, file.content_type, content, dest))

    staged: list[tuple[Evidence, bytes, Path]] = []
    for safe_name, content_type, content, dest in prepared:
        evidence = crud.evaluation.stage_evidence(
            db,
            response_id=response_id,
            file_path=str(dest),
            file_name=safe_name,
            file_type=content_type,
        )
        staged.append((evidence, content, dest))

    written: list[Path] = []
    try:
        for _, content, dest in staged:
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(content)
            written.append(dest)
    except OSError:
        for path in written:
            path.unlink(missing_ok=True)
        db.rollback()
        raise FileUploadError(f"No se pudo guardar el archivo '{dest.name}'")

    db.commit()
    for evidence, _, _ in staged:
        db.refresh(evidence)
    return [evidence for evidence, _, _ in staged]


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
