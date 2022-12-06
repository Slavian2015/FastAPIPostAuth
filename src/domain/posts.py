import uuid
from datetime import datetime
from typing import Optional

from src.domain.users import User
from src.value_object.value_object import PostTitle
from src.value_object.value_object import PostDescription


class Post:
    def __init__(
            self,
            author: User,
            title: PostTitle,
            description: PostDescription
    ) -> None:
        self.id = f"{uuid.uuid4()}"
        self.author = author
        self.title = str(title)
        self.description = str(description)
        self.date_created = datetime.now()
        self.date_updated: Optional[datetime] = None
        self.date_deleted: Optional[datetime] = None
        self.post_likes: list[PostLike] = []
        self.add_user_activity()

    def add_user_activity(self) -> None:
        self.author.update_last_request()

    def add_like(self, user: User) -> None:
        self.post_likes.append(PostLike(user, self))

    def delete_like(self, user: User) -> None:
        found_like = next(filter(lambda l: l.user == user, self.post_likes), None)
        if found_like is not None:
            self.post_likes.remove(found_like)


class PostLike:
    def __init__(self, user: User, post: Post) -> None:
        self.id = f"{uuid.uuid4()}"
        self.user = user
        self.post = post
        self.date_created = datetime.now()
