from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse


class AppError(Exception):
    """Базовая ошибка бизнес-логики.

    Сервисы бросают наследников этого класса, а обработчик, зарегистрированный
    в main, превращает их в HTTP-ответ вида {"detail": ...}.
    """

    status_code: int = status.HTTP_400_BAD_REQUEST
    detail: str = "Bad request"

    def __init__(self, detail: str | None = None, headers: dict[str, str] | None = None):
        if detail is not None:
            self.detail = detail
        self.headers = headers
        super().__init__(self.detail)


class NotFoundError(AppError):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Not found"


class AlreadyExistsError(AppError):
    status_code = status.HTTP_409_CONFLICT
    detail = "Already exists"


class RelatedObjectsError(AppError):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Object has related records"


class AuthenticationError(AppError):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Could not validate credentials"

    def __init__(self, detail: str | None = None):
        super().__init__(detail, headers={"WWW-Authenticate": "Bearer"})


class PermissionDeniedError(AppError):
    status_code = status.HTTP_403_FORBIDDEN
    detail = "Not enough permissions"


async def app_error_handler(request: Request, exc: AppError) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
        headers=exc.headers,
    )


def register_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(AppError, app_error_handler)
