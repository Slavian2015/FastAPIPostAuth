from __future__ import annotations
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy import Table
from sqlalchemy import DateTime

from src.domain.posts import Post
from src.domain.posts import PostLike
from src.domain.users import User
from src.mapping import PublicMetadata
from sqlalchemy.orm import registry
from sqlalchemy.orm import relationship
from sqlalchemy.types import CHAR

from src.mapping.users import UsersTable

PostsTable = Table(
    'posts', PublicMetadata,
    Column('id', CHAR(32), primary_key=True, index=True),
    Column("author_id", ForeignKey(UsersTable.c.id, ondelete='CASCADE'), nullable=False),
    Column('title', String(length=255), nullable=True, unique=True),
    Column('description', String(length=255)),
    Column('date_created', DateTime, nullable=False),
    Column('date_updated', DateTime, nullable=True),
    Column('date_deleted', DateTime, nullable=True),
)

PostLikesTable = Table(
    'likes', PublicMetadata,
    Column('id', CHAR(32), primary_key=True, index=True),
    Column('user_id', ForeignKey(UsersTable.c.id, ondelete='CASCADE'), nullable=False),
    Column('post_id', ForeignKey(PostsTable.c.id, ondelete='CASCADE'), nullable=False),
    Column('date_created', DateTime, nullable=False),
)


def perform_mapping() -> None:
    mapper_registry = registry()
    mapper_registry.map_imperatively(
        Post,
        PostsTable,
        properties={
            'author': relationship(User),
            'post_likes': relationship(PostLike,
                                       cascade="all, delete-orphan",
                                       back_populates="post"),
        }
    )

    mapper_registry.map_imperatively(PostLike, PostLikesTable, properties={
        'post': relationship(Post),
        'user': relationship(User)
    })
