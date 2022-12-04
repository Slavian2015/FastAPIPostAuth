from typing import Callable

from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker

from src.domain.users import User


def test_get_user_details(
        session_factory: sessionmaker,
        api_client: TestClient,
        user_factory: Callable[..., User],
        authorization_hash_factory: Callable[..., str],
        plaint_password: str
) -> None:
    with session_factory() as s:
        user = user_factory(password=plaint_password)
        s.add(user)
        s.commit()

        response = api_client.get('/users/me',
                                  headers={'Authorization': 'bearer %s' % authorization_hash_factory(user)})
        assert response.status_code == 200
        uploaded_data = response.json()
        assert uploaded_data["id"] == user.id
        assert uploaded_data["email"] == user.email
        s.delete(user)
        s.commit()
