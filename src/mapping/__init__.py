# flake8: noqa

from sqlalchemy import MetaData

PublicMetadata = MetaData()

from src.mapping import users


def perform_mapping() -> None:
    users.perform_mapping()
