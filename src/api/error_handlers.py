from fastapi import status
from fastapi.encoders import jsonable_encoder
from fastapi.requests import Request
from starlette.responses import JSONResponse


class DomainError(RuntimeError):
    pass


class AuthorizationError(RuntimeError):
    pass


class InvalidExpiredPasswordResetTokenError(RuntimeError):
    pass


class RequireValidationError(RuntimeError):
    pass


class AuthTokenError(RuntimeError):
    pass


class RequiredRegistrationError(RuntimeError):
    pass


async def http401_error_handler(_: Request, exc: AuthorizationError) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content=jsonable_encoder({'detail': {'error': str(exc)}}),
        headers={'WWW-Authenticate': 'Bearer'}
    )


async def http409_error_handler(_: Request, exc: DomainError) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content=jsonable_encoder({'detail': {'error': str(exc)}})
    )


async def http422_error_handler(_: Request, exc: InvalidExpiredPasswordResetTokenError) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({'detail': {'error': str(exc)}})
    )


async def http403_error_handler(_: Request, exc: RequireValidationError) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_403_FORBIDDEN,
        content=jsonable_encoder({'detail': {'error': str(exc)}})
    )
