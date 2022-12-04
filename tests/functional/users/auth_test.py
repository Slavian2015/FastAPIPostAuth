from typing import Callable
from sqlalchemy.orm import sessionmaker
from starlette.testclient import TestClient

from src.container import AppContainer
from src.domain.users import User
from src.handlers.interface import AuthTokenInterface


def test_auth(
        user_factory: Callable[..., User],
        session_factory: sessionmaker,
        app_container: AppContainer,
        api_client: TestClient,
        plaint_password: str
) -> None:
    with session_factory() as s:
        user = user_factory(password=plaint_password)
        s.add(user)
        s.commit()
        response = api_client.post('/auth', data={
            'username': user.email,
            'password': plaint_password
        })
        assert response.status_code == 200
        json = response.json()

        assert json['token_type'] == 'bearer'
        auth_token: AuthTokenInterface = app_container.security.auth_token()
        info = auth_token.get_user_info_from_token(json['access_token'])

        assert info.user_id == user.id
        s.delete(user)
        s.commit()
