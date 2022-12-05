from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

import src
from src.api.error_handlers import RequireValidationError
from src.api.error_handlers import AuthorizationError
from src.api.error_handlers import DomainError
from src.api.error_handlers import InvalidExpiredPasswordResetTokenError
from src.api.error_handlers import http401_error_handler
from src.api.error_handlers import http409_error_handler
from src.api.error_handlers import http422_error_handler
from src.api.error_handlers import http403_error_handler
import src.api.users.router as users_endpoints
import src.api.posts.router as posts_endpoints
import src.api.analitics.router as analytics_endpoints
import src.api.auth.router as auth_endpoints
from src.container import AppContainer
from src.mapping import perform_mapping

BASE_PATH = Path(__file__).parent.parent.parent.absolute()
load_dotenv(BASE_PATH / '.env')

container = AppContainer()

container.config.sqlite_dsn.from_env('SQLITE_DSN')

container.config.base_dir.from_value(BASE_PATH)
container.config.frontend_base_url.from_env('FRONTEND_BASE_URL', default='')

# Authorization
container.config.password_reset_token_expire.from_env('PASSWORD_RESET_TOKEN_EXPIRE', default=3600)
container.config.auth_secret.from_env('AUTH_SECRET')
container.config.auth_algo.from_env('AUTH_ALGORITHM')
container.config.auth_token_ttl.from_env('AUTH_TOKEN_TTL')


container.wire(packages=[src])
perform_mapping()

api = FastAPI()
api.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=["*"],
    allow_credentials=True,
    allow_headers=["*"],
)


@api.on_event('startup')
def startup() -> None:
    container.init_resources()


@api.on_event('shutdown')
def shutdown() -> None:
    container.shutdown_resources()


api.add_exception_handler(AuthorizationError, http401_error_handler)
api.add_exception_handler(DomainError, http409_error_handler)
api.add_exception_handler(InvalidExpiredPasswordResetTokenError, http422_error_handler)
api.add_exception_handler(RequireValidationError, http403_error_handler)

api.include_router(auth_endpoints.router, tags=['auth'])
api.include_router(users_endpoints.router, tags=['users'])
api.include_router(posts_endpoints.router, tags=['posts'])
api.include_router(analytics_endpoints.router, tags=['analytics'])
