from unittest.mock import MagicMock

import pytest
from fastapi.testclient import TestClient
from pytest_mock import MockerFixture

from src.api.auth.response import Token
from src.api.error_handlers import AuthorizationError
from src.api.error_handlers import DomainError
from src.container import AppContainer


@pytest.fixture
def auth_data() -> dict:
    return {'username': 'me@example.com', 'password': 's3cr3t'}


@pytest.fixture
def handler(mocker: MockerFixture) -> MagicMock:
    return mocker.patch('src.handlers.command.users.AuthorizeUserCommandHandler')


def test_unauthorized_response(
        auth_data: dict,
        handler: MagicMock,
        api_client: TestClient,
        app_container: AppContainer
) -> None:
    handler.handle.side_effect = AuthorizationError('Email or password is invalid')
    with app_container.handlers.container.authorization_command_handler.override(handler):
        response = api_client.post('/auth', data=auth_data)

    assert 401 == response.status_code
    assert {'detail': {'error': 'Email or password is invalid'}} == response.json()


def test_conflict_response(
        auth_data: dict,
        handler: MagicMock,
        api_client: TestClient,
        app_container: AppContainer
) -> None:
    handler.handle.side_effect = DomainError('domain error')
    with app_container.handlers.container.authorization_command_handler.override(handler):
        response = api_client.post('/auth', data=auth_data)

    assert 409 == response.status_code
    assert {'detail': {'error': 'domain error'}} == response.json()


def test_api_token_is_returned(
        auth_data: dict,
        handler: MagicMock,
        api_client: TestClient,
        app_container: AppContainer
) -> None:
    token = Token(access_token='some-hash', token_type='bearer')
    handler.handle.return_value = token
    with app_container.handlers.container.authorization_command_handler.override(handler):
        response = api_client.post('/auth', data=auth_data)

    assert response.status_code == 200
    assert response.json() == {
        'access_token': token.access_token,
        'token_type': token.token_type
    }
