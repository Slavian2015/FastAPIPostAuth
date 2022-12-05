from __future__ import annotations

from src.domain.posts import Post
from src.domain.users import User
from src.mapping.posts import PostsTable
from src.repositories.abstract import AbstractAlchemyRepository
from src.repositories.errors import PostNotExistsError
from src.repositories.errors import UserNotExistsError
from src.repositories.errors import PostExistsError
from src.repositories.interface import PostsRepositoryInterface


class PostsRepository(AbstractAlchemyRepository, PostsRepositoryInterface):

    def get_post_by_id(self, post_id: str) -> Post:
        post: Post | None = self.session.get(Post, post_id)
        if not post:
            raise PostNotExistsError
        return post

    def get_post_by_title(self, title: str) -> Post:
        post: Post | None = self.session.query(Post).where(PostsTable.c.title == title).one_or_none()
        if not post:
            raise PostNotExistsError
        return post

    def create_post(self, post: Post) -> str:
        try:
            self.get_post_by_title(post.title)
            raise PostExistsError('Post already exists')
        except PostNotExistsError:
            ...
        self.session.add(post)
        return post.id

    def get_user_by_id(self, user_id: str) -> User:
        user: User | None = self.session.get(User, user_id)
        if not user:
            raise UserNotExistsError
        return user
