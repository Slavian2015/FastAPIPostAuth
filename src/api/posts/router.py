from dependency_injector.wiring import Provide
from dependency_injector.wiring import inject
from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import Depends
from starlette import status

from src.api.auth.router import get_user_id_from_token
from src.api.posts.request import CreatePostRequest
from src.api.posts.response import GetPostDetailsResponse
from src.command.posts import CreatePostCommand
from src.container import AppContainer
from src.handlers.interface import CommandHandlerInterface
from src.repositories.errors import PersistenceError

router = APIRouter()


@router.post('/posts', response_model=GetPostDetailsResponse)
@inject
def create_post(
        request: CreatePostRequest,
        current_user_id: str = Depends(get_user_id_from_token),
        handler: CommandHandlerInterface[CreatePostCommand, GetPostDetailsResponse] =
        Depends(Provide[AppContainer.handlers.create_post])
) -> GetPostDetailsResponse:
    try:
        post_data = handler.handle(CreatePostCommand(
            user_id=current_user_id,
            title=request.title,
            description=request.description,
        ))
    except PersistenceError:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return post_data
