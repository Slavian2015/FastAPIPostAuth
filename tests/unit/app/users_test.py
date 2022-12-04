import pytest
from faker import Faker
from src.api.users.request import CreateUserRequest
from src.command.users import CreateUserCommand
from pydantic import EmailStr


@pytest.fixture
def request_data() -> dict:
    return {"email": 'me@example.com', "password": '123QWEasdzxc@'}


@pytest.fixture
def registration_command(faker: Faker) -> CreateUserCommand:
    return CreateUserCommand(email=faker.email(), password='p@assW0rd')


@pytest.mark.parametrize('password', [('qweasdzxc',), ('123qweasd',), ('qwASDzxc',), ('1Qa',)])
def test_invalid_password_raise_error(password: str) -> None:
    with pytest.raises(ValueError):
        CreateUserRequest(email=EmailStr('test@example.com'), password=password)


def test_valid_password_returned() -> None:
    req = CreateUserRequest(email=EmailStr('test@example.com'), password='123QWEasdzxc@')
    assert req.password == '123QWEasdzxc@'
