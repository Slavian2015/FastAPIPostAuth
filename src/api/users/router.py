from uuid import UUID

from dependency_injector.wiring import Provide
from dependency_injector.wiring import inject
from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import Depends
from starlette import status

from src.api.auth.router import get_user_id_from_token
from src.api.users.response import GetUserDetailsResponse
from src.api.users.response import DeleteUserResponse
from src.command.users import DeleteUserCommand
from src.container import AppContainer
from src.handlers.interface import CommandHandlerInterface
from src.handlers.interface import QueryHandlerInterface
from src.query.users import GetUserDetailsQuery
from src.repositories.errors import PersistenceError

router = APIRouter()


@router.delete('/users/{user_id}', response_model=DeleteUserResponse)
@inject
def delete_user(
        user_id: UUID,
        admin_id: UUID = Depends(get_user_id_from_token),
        handler: CommandHandlerInterface[DeleteUserCommand, None] =
        Depends(Provide[AppContainer.handlers.delete_user])
) -> DeleteUserResponse:
    try:
        handler.handle(DeleteUserCommand(admin_id=admin_id, user_id=user_id))
    except PersistenceError:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return DeleteUserResponse()


@router.get('/users/me', response_model=GetUserDetailsResponse)
@inject
def get_me(
        user_id: UUID = Depends(get_user_id_from_token),
        handler: QueryHandlerInterface[GetUserDetailsQuery, GetUserDetailsResponse] =
        Depends(Provide[AppContainer.handlers.get_me])
) -> GetUserDetailsResponse:
    try:
        found_user = handler.handle(GetUserDetailsQuery(user_id=user_id))
    except PersistenceError:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return found_user
