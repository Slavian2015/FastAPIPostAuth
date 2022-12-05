from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from src.api.users.response import GetUserCardResponse
from src.domain.posts import Post


class UpdatePostResponse(BaseModel):
    status: str = 'OK'


class GetPostDetailsResponse(BaseModel):
    id: str
    title: str
    description: str
    author: GetUserCardResponse
    date_created: datetime
    date_updated: Optional[datetime]
    date_deleted: Optional[datetime]

    @staticmethod
    def from_data(post: Post) -> GetPostDetailsResponse:
        return GetPostDetailsResponse(
            id=post.id,
            title=post.title,
            description=post.description,
            author=GetUserCardResponse.from_data(post.author),
            date_created=post.date_created,
            date_updated=post.date_updated,
            date_deleted=post.date_deleted,
        )
