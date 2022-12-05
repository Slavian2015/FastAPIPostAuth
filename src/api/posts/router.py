from dependency_injector.wiring import Provide
from dependency_injector.wiring import inject
from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import Depends
from starlette import status

from src.api.auth.router import get_user_id_from_token
from src.api.posts.request import CreatePostRequest
from src.api.posts.response import GetPostDetailsResponse
from src.api.posts.response import UpdatePostResponse
from src.command.posts import CreatePostCommand
from src.command.posts import LikePostCommand
from src.command.posts import UnLikePostCommand
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


@router.patch('/posts/like/{post_id}', response_model=UpdatePostResponse)
@inject
def like_post(
        post_id: str,
        current_user_id: str = Depends(get_user_id_from_token),
        handler: CommandHandlerInterface[LikePostCommand, None] =
        Depends(Provide[AppContainer.handlers.like_post])
) -> UpdatePostResponse:
    try:
        handler.handle(LikePostCommand(post_id=post_id, user_id=current_user_id))
    except PersistenceError:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return UpdatePostResponse()


@router.patch('/posts/unlike/{post_id}', response_model=UpdatePostResponse)
@inject
def unlike_post(
        post_id: str,
        current_user_id: str = Depends(get_user_id_from_token),
        handler: CommandHandlerInterface[UnLikePostCommand, None] =
        Depends(Provide[AppContainer.handlers.unlike_post])
) -> UpdatePostResponse:
    try:
        handler.handle(UnLikePostCommand(post_id=post_id, user_id=current_user_id))
    except PersistenceError:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return UpdatePostResponse()
