from typing import Callable, Any
from typing import Generator

from faker import Faker
from passlib.context import CryptContext
from starlette.testclient import TestClient

from src.api.application import api
from src.container import AppContainer
from src.handlers.interface import AuthTokenInterface

import pytest
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session
from src.api.application import container
from src.domain.users import User
from src.value_object.value_object import Email
from src.value_object.value_object import PlainPassword


@pytest.fixture(scope='module')
def app_container() -> Generator:
    yield container


@pytest.fixture
def api_client() -> TestClient:
    return TestClient(api)


@pytest.fixture
def session_factory() -> Callable[..., Session]:
    return sessionmaker(bind=container.sqlalchemy_engine())


@pytest.fixture
def authorization_hash_factory(app_container: AppContainer) -> Callable[[User], str]:
    def maker(user: User) -> str:
        auth_token: AuthTokenInterface = app_container.security.auth_token()
        token = auth_token.generate_token(user.id)
        return token.access_token

    return maker


@pytest.fixture
def authorization_hash(
        authorization_hash_factory: Callable[..., str],
        persisted_user: User
) -> str:
    return authorization_hash_factory(persisted_user)


@pytest.fixture
def plaint_password(faker: Faker) -> str:
    return faker.password()


@pytest.fixture
def user_factory(faker: Faker) -> Callable[..., User]:
    def maker(**kwargs: Any) -> User:
        user = User(
            email=Email(faker.email()),
            password=kwargs.get("password", PlainPassword(faker.password())),
            hasher=CryptContext(schemes=['argon2']),
        )
        return user
    return maker
