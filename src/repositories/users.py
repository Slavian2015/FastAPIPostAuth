from __future__ import annotations

from src.domain.users import User
from src.mapping.users import UsersTable
from src.repositories.abstract import AbstractAlchemyRepository
from src.repositories.errors import UserNotExistsError
from src.repositories.errors import UserExistsError
from src.repositories.interface import UsersRepositoryInterface


class UsersRepository(AbstractAlchemyRepository, UsersRepositoryInterface):

    def get_user_by_id(self, user_id: str) -> User:
        user: User | None = self.session.get(User, user_id)
        if not user:
            raise UserNotExistsError
        return user

    def get_user_by_email(self, email: str) -> User:
        user: User | None = self.session.query(User).where(UsersTable.c.email == email).one_or_none()
        if not user:
            raise UserNotExistsError
        return user

    def create_user(self, user: User) -> str:
        try:
            self.get_user_by_email(user.email)
            raise UserExistsError('User already exist')
        except UserNotExistsError:
            ...
        self.session.add(user)
        return user.id
