import pytest
from passlib.context import CryptContext
import secrets


@pytest.fixture(scope='session')
def password_hasher() -> CryptContext:
    return CryptContext(schemes=['argon2'])


@pytest.fixture
def dummy_token() -> str:
    return secrets.token_urlsafe(64)
