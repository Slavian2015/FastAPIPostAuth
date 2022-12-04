import uuid
import secrets
import base64
import random
from datetime import datetime
from typing import Optional
from dependency_injector.wiring import inject
from dependency_injector.wiring import Provide
from passlib.context import CryptContext
from sqlalchemy.orm import reconstructor

from src.value_object.value_object import Email
from src.value_object.value_object import PlainPassword

TOKEN_REGEXP = r'^[\w\-]+$'


def get_random_token() -> str:
    return secrets.token_urlsafe(64)


class User:
    def __init__(
            self,
            email: Email,
            password: PlainPassword,
            hasher: CryptContext,
    ) -> None:
        self.id = f"{uuid.uuid4()}"
        self.email = str(email)
        self.password_hasher = hasher
        self.password = self.password_hasher.hash(str(password))
        self.verification_token = base64.b64encode(
            random.getrandbits(512).to_bytes(64, byteorder='big')
        ).decode('utf-8')

        self.date_created = datetime.now()
        self.date_logged = self.date_created
        self.date_updated: Optional[datetime] = None
        self.date_deleted: Optional[datetime] = None

    @inject
    @reconstructor
    def __orm_init__(
            self,
            hasher: CryptContext = Provide['security_context'],  # pragma: no cover
    ) -> None:
        self.password_hasher = hasher

    def verify_hash(self, verification_hash: str) -> bool:
        return self.verification_token == verification_hash

    def authorize(self, plain_password: str) -> bool:
        return self.password_hasher.verify(plain_password, self.password)

    def update_logged_date(self) -> None:
        self.date_logged = datetime.now()

    def delete_user(self) -> None:
        self.date_deleted = datetime.now()
