from pydantic import BaseModel


class StructBase(BaseModel):
    class Config:
        allow_mutation = False


class AuthTokenClaimsStruct(StructBase):
    sub: str
    exp: int
    iat: int


class TokenStruct(StructBase):
    access_token: str
    token_type: str


class AuthTokenUserInfoStruct(StructBase):
    user_id: str
