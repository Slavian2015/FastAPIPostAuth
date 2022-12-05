import datetime
from typing import Callable

from faker import Faker
from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker

from src.domain.posts import Post
from src.domain.posts import PostLike
from src.domain.users import User


def test_get_analytics(
        session_factory: sessionmaker,
        api_client: TestClient,
        post_factory: Callable[..., Post],
        authorization_hash_factory: Callable[..., str],
        faker: Faker
) -> None:
    with session_factory() as s:
        post = post_factory()

        like1 = PostLike(post.author, post)
        like2 = PostLike(post.author, post)
        like3 = PostLike(post.author, post)

        like1.date_created = datetime.datetime(year=2020, month=1, day=29, hour=13, minute=14, second=31)
        like2.date_created = datetime.datetime(year=2020, month=1, day=30, hour=13, minute=14, second=31)
        like3.date_created = datetime.datetime(year=2020, month=1, day=31, hour=13, minute=14, second=31)

        post.post_likes.append(like1)
        post.post_likes.append(like2)
        post.post_likes.append(like3)
        s.add(post)
        s.commit()

        assert len(post.post_likes) == 3

        payload: dict = {
            "date_from": str(datetime.date(year=2020, month=1, day=28)),
            "date_to": str(datetime.date(year=2020, month=1, day=31))
        }

        response = api_client.post('/analytics', json=payload)

        assert response.status_code == 200
        uploaded_data = response.json()

        assert len(uploaded_data["likes"]) == 3
        assert uploaded_data["likes"][0]["qty"] == 1

        list(map(s.delete, [post, post.author]))
        s.commit()


def test_get_aggregated_analytics(
        session_factory: sessionmaker,
        api_client: TestClient,
        post_factory: Callable[..., Post],
        authorization_hash_factory: Callable[..., str],
        faker: Faker
) -> None:
    with session_factory() as s:
        post = post_factory()

        like1 = PostLike(post.author, post)
        like2 = PostLike(post.author, post)
        like3 = PostLike(post.author, post)

        like1.date_created = datetime.datetime(year=2020, month=1, day=30, hour=10, minute=14, second=31)
        like2.date_created = datetime.datetime(year=2020, month=1, day=30, hour=11, minute=14, second=31)
        like3.date_created = datetime.datetime(year=2020, month=1, day=30, hour=13, minute=14, second=31)

        post.post_likes.append(like1)
        post.post_likes.append(like2)
        post.post_likes.append(like3)
        s.add(post)
        s.commit()

        assert len(post.post_likes) == 3

        payload: dict = {
            "date_from": str(datetime.date(year=2020, month=1, day=28)),
            "date_to": str(datetime.date(year=2020, month=1, day=31))
        }

        response = api_client.post('/analytics', json=payload)

        assert response.status_code == 200
        uploaded_data = response.json()

        assert len(uploaded_data["likes"]) == 1
        assert uploaded_data["likes"][0]["qty"] == 3

        list(map(s.delete, [post, post.author]))
        s.commit()


def test_get_analytics_out_of_range(
        session_factory: sessionmaker,
        api_client: TestClient,
        post_factory: Callable[..., Post],
        authorization_hash_factory: Callable[..., str],
        faker: Faker
) -> None:
    with session_factory() as s:
        post = post_factory()

        like1 = PostLike(post.author, post)
        like2 = PostLike(post.author, post)
        like3 = PostLike(post.author, post)

        like1.date_created = datetime.datetime(year=2019, month=1, day=30, hour=10, minute=14, second=31)
        like2.date_created = datetime.datetime(year=2020, month=1, day=30, hour=11, minute=14, second=31)
        like3.date_created = datetime.datetime(year=2020, month=1, day=30, hour=13, minute=14, second=31)

        post.post_likes.append(like1)
        post.post_likes.append(like2)
        post.post_likes.append(like3)
        s.add(post)
        s.commit()

        assert len(post.post_likes) == 3

        payload: dict = {
            "date_from": str(datetime.date(year=2020, month=1, day=28)),
            "date_to": str(datetime.date(year=2020, month=1, day=31))
        }

        response = api_client.post('/analytics', json=payload)

        assert response.status_code == 200
        uploaded_data = response.json()

        assert len(uploaded_data["likes"]) == 1
        assert uploaded_data["likes"][0]["qty"] == 2

        list(map(s.delete, [post, post.author]))
        s.commit()


def test_get_user_activity(
        session_factory: sessionmaker,
        api_client: TestClient,
        user_factory: Callable[..., User],
        authorization_hash_factory: Callable[..., str],
        plaint_password: str
) -> None:
    with session_factory() as s:
        user = user_factory()
        user2 = user_factory()

        user.date_updated = datetime.datetime(year=2019, month=1, day=30)
        user2.date_updated = datetime.datetime(year=2020, month=1, day=30)

        s.add_all([user, user2])
        s.commit()

        response = api_client.get(f'/analytics/activity/{user.id}')

        assert response.status_code == 200
        uploaded_data = response.json()
        assert uploaded_data["last_login"] == str(user.date_logged.date())
        assert uploaded_data["last_request"] == str(user.date_updated.date())
        s.delete(user)
        s.delete(user2)
        s.commit()
