from __future__ import annotations

from passlib.context import CryptContext
from sqlalchemy.exc import SQLAlchemyError

from src.api.auth.response import Token
from src.api.error_handlers import AuthorizationError
from src.api.error_handlers import DomainError
from src.command.users import DeleteUserCommand
from src.command.users import CreateUserCommand
from src.command.users import AuthorizeUserCommand

from src.api.users.response import GetUserDetailsResponse
from src.handlers.interface import CommandHandlerInterface
from src.handlers.interface import AuthTokenInterface
from src.repositories.errors import UserNotExistsError
from src.repositories.errors import UserExistsError
from src.repositories.interface import UsersRepositoryInterface
from src.value_object.value_object import PlainPassword
from src.value_object.value_object import Email
from src.domain.users import User


class CreateUserCommandHandler(CommandHandlerInterface):
    def __init__(
            self,
            user_repository: UsersRepositoryInterface,
            security_context: CryptContext,
            auth: AuthTokenInterface,
    ) -> None:
        self.user_repository = user_repository
        self.__security_context = security_context
        self.__auth = auth

    def handle(self, command: CreateUserCommand) -> GetUserDetailsResponse:
        with self.user_repository.autocommit():
            try:
                user = self.create_user(command)
                response = GetUserDetailsResponse.from_data(user)
            except SQLAlchemyError:
                raise DomainError('Failed to create user')
            except UserExistsError:
                raise DomainError('User already exists')
        return response

    def create_user(self, command: CreateUserCommand) -> User:
        user = User(
            email=Email(command.email),
            password=PlainPassword(command.password),
            hasher=self.__security_context,
        )

        self.user_repository.create_user(user)
        return user


class DeleteUserCommandHandler(CommandHandlerInterface):
    def __init__(self, user_repository: UsersRepositoryInterface) -> None:
        self.user_repository = user_repository

    def handle(self, command: DeleteUserCommand) -> None:
        with self.user_repository.autocommit():
            try:
                user = self.user_repository.get_user_by_id(command.user_id)
                user.delete_user()
            except SQLAlchemyError:
                raise DomainError('Failed to delete User')


class AuthorizeUserCommandHandler(CommandHandlerInterface):
    def __init__(self, user_repository: UsersRepositoryInterface, auth: AuthTokenInterface) -> None:
        self.__auth = auth
        self.user_repository = user_repository

    def handle(self, command: AuthorizeUserCommand) -> Token:
        with self.user_repository.autocommit():
            try:
                user: User = self.user_repository.get_user_by_email(command.email)

                if not user.authorize(command.plain_password):
                    raise AuthorizationError('login or password is invalid')
                token = self.__get_auth_token(user)

            except AuthorizationError as e:
                raise DomainError(str(e))
            except UserNotExistsError as e:
                raise DomainError(str(e))
            except SQLAlchemyError:
                raise DomainError('Failed authorization, because of internal error')
        return token

    def __get_auth_token(self, user: User) -> Token:
        token_credentials = self.__auth.generate_token(user.id)
        return Token(**token_credentials.dict())
