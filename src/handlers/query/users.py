from sqlalchemy.exc import SQLAlchemyError

from src.api.error_handlers import DomainError
from src.api.users.response import GetUserDetailsResponse
from src.handlers.interface import CommandHandlerInterface
from src.query.users import GetUserDetailsQuery
from src.repositories.errors import UserNotExistsError
from src.repositories.interface import UsersRepositoryInterface


class GetUserDetailsQueryHandler(CommandHandlerInterface):
    def __init__(self, user_repository: UsersRepositoryInterface) -> None:
        self.user_repository = user_repository

    def handle(self, query: GetUserDetailsQuery) -> GetUserDetailsResponse:
        with self.user_repository.autocommit():
            try:
                user = self.user_repository.get_user_by_id(query.user_id)
                found_data = GetUserDetailsResponse.from_data(user)
            except SQLAlchemyError:
                raise DomainError('Failed to get user information')
            except UserNotExistsError as e:
                raise DomainError(str(e))
        return found_data
