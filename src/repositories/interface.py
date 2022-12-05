from __future__ import annotations

from abc import abstractmethod
from types import TracebackType
from typing import Any
from typing import Optional
from typing import Protocol
from typing import Type

from src.domain.posts import Post
from src.domain.users import User
from src.query.analytics import GetAnalyticsQuery


class AutocommitInterface(Protocol):
    @abstractmethod
    def autocommit(self) -> Any:
        raise NotImplementedError

    @abstractmethod
    def __enter__(self) -> Any:
        raise NotImplementedError

    @abstractmethod
    def __exit__(
            self,
            exc_type: Optional[Type[BaseException]],
            exc_val: Optional[BaseException],
            exc_tb: Optional[TracebackType]
    ) -> bool:
        raise NotImplementedError


class UsersRepositoryInterface(AutocommitInterface):

    @abstractmethod
    def create_user(self, user: User) -> str:
        raise NotImplementedError

    @abstractmethod
    def get_user_by_email(self, email: str) -> User:
        raise NotImplementedError

    @abstractmethod
    def get_user_by_id(self, user_id: str) -> User:
        raise NotImplementedError


class PostsRepositoryInterface(AutocommitInterface):

    @abstractmethod
    def create_post(self, post: Post) -> str:
        raise NotImplementedError

    @abstractmethod
    def get_post_by_title(self, title: str) -> Post:
        raise NotImplementedError

    @abstractmethod
    def get_post_by_id(self, post_id: str) -> Post:
        raise NotImplementedError

    @abstractmethod
    def get_user_by_id(self, user_id: str) -> User:
        raise NotImplementedError


class AnalyticsRepositoryInterface(AutocommitInterface):

    @abstractmethod
    def get_post_by_id(self, post_id: str) -> Post:
        raise NotImplementedError

    @abstractmethod
    def get_user_by_id(self, user_id: str) -> User:
        raise NotImplementedError

    @abstractmethod
    def get_analytics_by_filter(self, query: GetAnalyticsQuery) -> dict:
        raise NotImplementedError
