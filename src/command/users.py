from pydantic import BaseModel


class CreateUserCommand(BaseModel):
    email: str
    password: str


class EmailValidationCommand(BaseModel):
    hash: str


class AuthorizeUserCommand(BaseModel):
    email: str
    plain_password: str


class DeleteUserCommand(BaseModel):
    user_id: str
