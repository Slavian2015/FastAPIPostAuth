from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer
from sqlalchemy.orm.scoping import ScopedSession

from src.repositories.posts import PostsRepository
from src.repositories.users import UsersRepository
from src.repositories.analytics import AnalyticsRepository


class RepositoriesContainer(DeclarativeContainer):
    sqlalchemy_session = providers.Dependency(instance_of=ScopedSession)

    users = providers.Factory(UsersRepository, session=sqlalchemy_session)
    posts = providers.Factory(PostsRepository, session=sqlalchemy_session)
    analytics = providers.Factory(AnalyticsRepository, session=sqlalchemy_session)
