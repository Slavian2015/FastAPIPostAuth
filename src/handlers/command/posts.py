from sqlalchemy.exc import SQLAlchemyError

from src.api.error_handlers import DomainError
from src.api.posts.response import GetPostDetailsResponse
from src.command.posts import CreatePostCommand
from src.domain.posts import Post
from src.handlers.interface import CommandHandlerInterface
from src.repositories.errors import PostExistsError
from src.repositories.interface import PostsRepositoryInterface
from src.value_object.value_object import PostTitle
from src.value_object.value_object import PostDescription
from src.domain.users import User


class CreatePostCommandHandler(CommandHandlerInterface):
    def __init__(self, post_repository: PostsRepositoryInterface) -> None:
        self.post_repository = post_repository

    def handle(self, command: CreatePostCommand) -> GetPostDetailsResponse:
        with self.post_repository.autocommit():
            try:
                author = self.post_repository.get_user_by_id(command.user_id)
                post = self.create_post(author, command)
                response = GetPostDetailsResponse.from_data(post)
            except SQLAlchemyError:
                raise DomainError('Failed to create post')
            except PostExistsError:
                raise DomainError('Post already exists')
        return response

    def create_post(self, author: User, command: CreatePostCommand) -> Post:
        post = Post(
            author=author,
            title=PostTitle(command.title),
            description=PostDescription(command.description),
        )
        self.post_repository.create_post(post)
        return post
