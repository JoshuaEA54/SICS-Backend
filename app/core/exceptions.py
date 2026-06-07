from http import HTTPStatus


class AppError(Exception):
    status_code: int

    def __init__(self, mensaje: str) -> None:
        self.mensaje = mensaje
        super().__init__(mensaje)


class NotFoundError(AppError):
    status_code = HTTPStatus.NOT_FOUND


class ConflictError(AppError):
    status_code = HTTPStatus.CONFLICT


class ReferenceError(AppError):
    status_code = HTTPStatus.UNPROCESSABLE_ENTITY


class FileUploadError(AppError):
    status_code = HTTPStatus.INTERNAL_SERVER_ERROR


class InvalidFileError(AppError):
    status_code = HTTPStatus.BAD_REQUEST


class UnauthorizedError(AppError):
    status_code = HTTPStatus.UNAUTHORIZED


class ForbiddenError(AppError):
    status_code = HTTPStatus.FORBIDDEN


class BadRequestError(AppError):
    status_code = HTTPStatus.BAD_REQUEST


class ServiceUnavailableError(AppError):
    status_code = HTTPStatus.BAD_GATEWAY
