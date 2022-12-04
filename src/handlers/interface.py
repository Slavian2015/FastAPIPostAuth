from abc import ABC
from abc import abstractmethod
from typing import Generic
from typing import TypeVar

from src.services.token import TokenStruct
from src.services.token import AuthTokenUserInfoStruct

TCommand = TypeVar('TCommand')
TQuery = TypeVar('TQuery')
TResult = TypeVar('TResult')


class QueryHandlerInterface(ABC, Generic[TQuery, TResult]):
    @abstractmethod
    def handle(self, query: TQuery) -> TResult:
        raise NotImplementedError


class CommandHandlerInterface(ABC, Generic[TCommand, TResult]):
    @abstractmethod
    def handle(self, command: TCommand) -> TResult:
        raise NotImplementedError


class AuthTokenInterface(ABC):
    def generate_token(self, sub: str) -> TokenStruct:
        raise NotImplementedError

    def get_user_info_from_token(self, token: str) -> AuthTokenUserInfoStruct:
        raise NotImplementedError
