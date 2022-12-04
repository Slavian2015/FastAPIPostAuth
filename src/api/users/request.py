from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import validator
import re

from src.domain.users import TOKEN_REGEXP
from src.value_object.value_object import PlainPassword


def validate_hash(token: str) -> str:
    if not re.match(TOKEN_REGEXP, token):
        raise ValueError('Incorrect hash')
    return token


class EmailHashValidationRequest(BaseModel):
    hash: str


class CreateUserRequest(BaseModel):
    email: EmailStr
    password: str

    @validator('password')
    def password_format(cls, password: str) -> str:
        return str(PlainPassword(password))
