from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer
from passlib.context import CryptContext

from src.handlers.command.posts import CreatePostCommandHandler
from src.handlers.command.posts import LikePostCommandHandler
from src.handlers.command.posts import UnLikePostCommandHandler
from src.handlers.command.users import AuthorizeUserCommandHandler
from src.handlers.command.users import CreateUserCommandHandler
from src.handlers.command.users import DeleteUserCommandHandler
from src.handlers.query.analytics import GetAnalyticsQueryHandler
from src.handlers.query.analytics import GetActivityQueryHandler
from src.handlers.query.users import GetUserDetailsQueryHandler


class HandlersContainer(DeclarativeContainer):
    repositories = providers.DependenciesContainer()
    password_reset_token_expire = providers.Dependency(instance_of=int)
    security_context = providers.Dependency(instance_of=CryptContext)
    services = providers.DependenciesContainer()
    security = providers.DependenciesContainer()

    authorization_command_handler = providers.Factory(
        AuthorizeUserCommandHandler,
        user_repository=repositories.users,
        auth=security.auth_token
    )

    create_user = providers.Factory(
        CreateUserCommandHandler,
        user_repository=repositories.users,
        security_context=security_context
    )

    get_me = providers.Factory(GetUserDetailsQueryHandler, user_repository=repositories.users)
    delete_user = providers.Factory(DeleteUserCommandHandler, user_repository=repositories.users)

    create_post = providers.Factory(CreatePostCommandHandler, post_repository=repositories.posts)
    like_post = providers.Factory(LikePostCommandHandler, post_repository=repositories.posts)
    unlike_post = providers.Factory(UnLikePostCommandHandler, post_repository=repositories.posts)

    get_analytics = providers.Factory(GetAnalyticsQueryHandler, analytic_repository=repositories.analytics)
    get_user_activity = providers.Factory(GetActivityQueryHandler, analytic_repository=repositories.analytics)
