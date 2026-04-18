from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from psycopg.errors import ForeignKeyViolation, UniqueViolation
from sqlalchemy.exc import IntegrityError, NoResultFound

from app.core.exceptions import AppError


def _error(status: int, message: str) -> JSONResponse:
    return JSONResponse(status_code=status, content={"detail": message})


async def _handle_app_error(_request: Request, exc: AppError) -> JSONResponse:
    return _error(exc.status_code, exc.mensaje)


async def _handle_not_found(_request: Request, _exc: NoResultFound) -> JSONResponse:
    return _error(404, "Recurso no encontrado")


async def _handle_integrity_error(_request: Request, exc: IntegrityError) -> JSONResponse:
    orig = getattr(exc, "orig", None)
    if isinstance(orig, UniqueViolation):
        return _error(409, "Ya existe un registro con esos datos")
    if isinstance(orig, ForeignKeyViolation):
        return _error(422, "Referencia a un elemento que no existe")
    return _error(409, "Error de integridad de datos")


async def _handle_validation_error(_request: Request, exc: RequestValidationError) -> JSONResponse:
    errores = [
        f"{' → '.join(str(loc) for loc in e['loc'])}: {e['msg']}"
        for e in exc.errors()
    ]
    return _error(422, f"Datos de entrada invalidos: {'; '.join(errores)}")


async def _handle_unexpected_error(_request: Request, _exc: Exception) -> JSONResponse:
    return _error(500, "Error interno del servidor")


def registrar_handlers(app: FastAPI) -> None:
    app.add_exception_handler(AppError, _handle_app_error)
    app.add_exception_handler(NoResultFound, _handle_not_found)
    app.add_exception_handler(IntegrityError, _handle_integrity_error)
    app.add_exception_handler(RequestValidationError, _handle_validation_error)
    app.add_exception_handler(Exception, _handle_unexpected_error)
