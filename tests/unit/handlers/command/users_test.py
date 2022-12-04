from unittest.mock import MagicMock

import pytest
from faker import Faker
from src.api.error_handlers import DomainError
from src.command.users import CreateUserCommand
from src.container import AppContainer
from src.handlers.command.users import CreateUserCommandHandler
from src.repositories.errors import UserExistsError
from src.repositories.interface import UsersRepositoryInterface


@pytest.fixture
def registration_command(faker: Faker) -> CreateUserCommand:
    return CreateUserCommand(email=faker.email(), password='p@assW0rd')


def test_create_user_command_handler(
        registration_command: CreateUserCommand,
        app_container: AppContainer
) -> None:
    repository = MagicMock(spec=UsersRepositoryInterface)
    handler = CreateUserCommandHandler(repository, MagicMock(), MagicMock())

    with app_container.repositories.users.override(MagicMock()):
        handler.handle(registration_command)
    assert repository.create_user.called


def test_existing_user_raise_exception(
        registration_command: CreateUserCommand,
        app_container: AppContainer
) -> None:
    repository = MagicMock(spec=UsersRepositoryInterface)
    repository.create_user.side_effect = UserExistsError

    handler = CreateUserCommandHandler(repository, MagicMock(), MagicMock())
    with pytest.raises(DomainError) as e:
        with app_container.repositories.users.override(MagicMock()):
            handler.handle(registration_command)
    assert str(e.value) == 'User already exists'
