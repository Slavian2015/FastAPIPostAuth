from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer
from sqlalchemy.orm.scoping import ScopedSession

from src.repositories.users import UsersRepository


class RepositoriesContainer(DeclarativeContainer):
    sqlalchemy_session = providers.Dependency(instance_of=ScopedSession)

    users = providers.Factory(UsersRepository, session=sqlalchemy_session)
