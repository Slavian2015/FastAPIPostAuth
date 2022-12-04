from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenResponse(Token):
    pass


class GeneralSuccessResponse(BaseModel):
    status: str = 'OK'
