from __future__ import annotations

from abc import ABC
from types import TracebackType
from typing import Optional
from typing import Type

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from sqlalchemy.orm import scoped_session

from src.repositories.errors import PersistenceError


class AbstractAlchemyRepository(ABC):
    def __init__(self, session: scoped_session) -> None:
        self.__autocommit_transaction = False
        self.session_factory = session
        self.session: Session = self.session_factory()

    def autocommit(self) -> AbstractAlchemyRepository:
        self.__autocommit_transaction = True
        return self

    def __enter__(self) -> AbstractAlchemyRepository:
        if not self.__autocommit_transaction:
            raise RuntimeError('Can not use class instance as a context manager. Use autocommit method instead')
        return self

    def __exit__(
            self,
            exc_type: Optional[Type[BaseException]],
            exc_val: Optional[BaseException],
            exc_tb: Optional[TracebackType]
    ) -> bool:
        self.__autocommit_transaction = False
        if exc_type:
            self.session_factory.remove()
            return False
        try:
            self.session.commit()
        except SQLAlchemyError:
            self.session.rollback()
            raise PersistenceError
        finally:
            self.session_factory.remove()
        return True
