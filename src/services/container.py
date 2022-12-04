from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer

from src.services.auth import AuthToken


class ServicesContainer(DeclarativeContainer):
    frontend_url = providers.Dependency(instance_of=str)


class Security(DeclarativeContainer):
    auth_secret_key = providers.Dependency(instance_of=str)
    auth_token_ttl = providers.Dependency(instance_of=int)

    auth_token = providers.Factory(
        AuthToken,
        auth_secret_key=auth_secret_key,
        auth_token_ttl=auth_token_ttl,
    )
