from dependency_injector.wiring import Provide
from dependency_injector.wiring import inject
from fastapi import APIRouter
from fastapi import Depends

from fastapi.security import OAuth2PasswordBearer
from fastapi.security import OAuth2PasswordRequestForm

from src.api.auth.response import TokenResponse
from src.api.error_handlers import AuthTokenError
from src.api.error_handlers import AuthorizationError
from src.command.users import AuthorizeUserCommand
from src.container import AppContainer
from src.handlers.interface import AuthTokenInterface
from src.handlers.interface import CommandHandlerInterface

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='auth')
optional_auth_scheme = OAuth2PasswordBearer(tokenUrl='auth', auto_error=False)


@inject
def get_user_id_from_token(
        token: str = Depends(oauth2_scheme),
        auth_token: AuthTokenInterface = Depends(
            Provide[AppContainer.security.auth_token]
        )
) -> str:
    try:
        auth_info = auth_token.get_user_info_from_token(token)
        return auth_info.user_id
    except AuthTokenError as e:
        raise AuthorizationError(str(e))


@router.post('/auth', response_model=TokenResponse)
@inject
def authorize_user(
        data: OAuth2PasswordRequestForm = Depends(),
        handler: CommandHandlerInterface[AuthorizeUserCommand, TokenResponse] = Depends(
            Provide[AppContainer.handlers.authorization_command_handler]
        )
) -> TokenResponse:
    command = AuthorizeUserCommand(email=data.username, plain_password=data.password)
    respond = handler.handle(command)
    return respond
