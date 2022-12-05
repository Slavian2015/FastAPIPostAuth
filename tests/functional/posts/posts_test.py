from typing import Callable

from faker import Faker
from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker

from src.domain.posts import Post
from src.domain.users import User


def test_create_new_post(
        session_factory: sessionmaker,
        api_client: TestClient,
        user_factory: Callable[..., User],
        authorization_hash_factory: Callable[..., str],
        faker: Faker
) -> None:
    with session_factory() as s:
        user = user_factory()
        s.add(user)
        s.commit()

        payload: dict = {
            "title": faker.word(),
            "description": faker.word()
        }

        response = api_client.post('/posts',
                                   headers={'Authorization': 'bearer %s' % authorization_hash_factory(user)},
                                   json=payload)

        assert response.status_code == 200
        json = response.json()
        assert 'id' in json.keys()
        post = s.query(Post).get(json['id'])
        assert post is not None
        assert post.title == payload["title"]
        s.refresh(user)

        list(map(s.delete, [post, user]))
        s.commit()


def test_like_post(
        session_factory: sessionmaker,
        api_client: TestClient,
        post_factory: Callable[..., Post],
        authorization_hash_factory: Callable[..., str],
        faker: Faker
) -> None:
    with session_factory() as s:
        post = post_factory()
        s.add(post)
        s.commit()

        response = api_client.patch(f'/posts/like/{post.id}',
                                    headers={'Authorization': 'bearer %s' % authorization_hash_factory(post.author)})

        assert response.status_code == 200
        s.refresh(post)

        assert len(post.post_likes) == 1
        assert post.post_likes[0].user.id == post.author.id

        list(map(s.delete, [post.post_likes[0], post, post.author]))
        s.commit()


def test_unlike_post(
        session_factory: sessionmaker,
        api_client: TestClient,
        post_factory: Callable[..., Post],
        authorization_hash_factory: Callable[..., str],
        faker: Faker
) -> None:
    with session_factory() as s:
        post = post_factory()
        post.add_like(post.author)
        s.add(post)
        s.commit()

        assert len(post.post_likes) == 1

        response = api_client.patch(f'/posts/unlike/{post.id}',
                                    headers={'Authorization': 'bearer %s' % authorization_hash_factory(post.author)})

        assert response.status_code == 200
        s.refresh(post)

        assert len(post.post_likes) == 0

        list(map(s.delete, [post, post.author]))
        s.commit()
