from __future__ import annotations

from sqlalchemy import select
from sqlalchemy import func
from sqlalchemy import distinct
from sqlalchemy.sql.functions import count

from src.domain.posts import Post
from src.domain.users import User
from src.mapping.posts import PostLikesTable
from src.query.analytics import GetAnalyticsQuery
from src.repositories.abstract import AbstractAlchemyRepository
from src.repositories.errors import PostNotExistsError
from src.repositories.errors import UserNotExistsError
from src.repositories.interface import AnalyticsRepositoryInterface


class AnalyticsRepository(AbstractAlchemyRepository, AnalyticsRepositoryInterface):

    def get_post_by_id(self, post_id: str) -> Post:
        post: Post | None = self.session.get(Post, post_id)
        if not post:
            raise PostNotExistsError
        return post

    def get_user_by_id(self, user_id: str) -> User:
        user: User | None = self.session.get(User, user_id)
        if not user:
            raise UserNotExistsError
        return user

    def get_analytics_by_filter(self, query: GetAnalyticsQuery) -> dict:

        stmt = select(func.date(PostLikesTable.c.date_created).label("date"),
                      count(distinct(PostLikesTable.c.id)).label("qty"))\
            .group_by(func.date(PostLikesTable.c.date_created))

        stmt = stmt.where(func.date(PostLikesTable.c.date_created) >= query.date_from,
                          func.date(PostLikesTable.c.date_created) <= query.date_to)

        return dict([(r["date"], r["qty"]) for r in self.session.execute(stmt).all()])
