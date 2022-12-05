# flake8: noqa

from sqlalchemy import MetaData


PublicMetadata = MetaData()

from src.mapping import users
from src.mapping import posts


def perform_mapping() -> None:
    users.perform_mapping()
    posts.perform_mapping()
