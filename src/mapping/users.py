from __future__ import annotations
from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Table
from sqlalchemy import DateTime

from src.domain.users import User
from src.mapping import PublicMetadata
from sqlalchemy.orm import registry
from sqlalchemy.types import CHAR

UsersTable = Table(
    'users', PublicMetadata,
    Column('id', CHAR(32), primary_key=True, index=True),
    Column('email', String(length=255), nullable=True, unique=True),
    Column('password', String(length=255)),
    Column('verification_token', String, nullable=True),
    Column('date_created', DateTime, nullable=False),
    Column('date_updated', DateTime, nullable=True),
    Column('date_deleted', DateTime, nullable=True),
    Column('date_logged', DateTime, nullable=False),
)


def perform_mapping() -> None:
    mapper_registry = registry()
    mapper_registry.map_imperatively(User, UsersTable)
