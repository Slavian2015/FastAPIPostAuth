from time import time
from typing import Union
from jose import JWTError
from jose import jwt

from src.api.error_handlers import AuthTokenError
from src.handlers.interface import AuthTokenInterface
from src.services.token import AuthTokenClaimsStruct
from src.services.token import TokenStruct
from src.services.token import AuthTokenUserInfoStruct


class AuthToken(AuthTokenInterface):
    def __init__(
            self,
            auth_secret_key: str,
            auth_token_ttl: int,
            algorithms: Union[str, list] = 'HS256'
    ) -> None:
        self._algorithms = algorithms
        self._auth_secret_key = auth_secret_key
        self._auth_token_ttl = auth_token_ttl

    def _decode(self, key: str) -> AuthTokenClaimsStruct:
        try:
            return AuthTokenClaimsStruct(
                **jwt.decode(
                    key,
                    self._auth_secret_key,
                    algorithms=self._algorithms
                )
            )
        except JWTError as e:
            raise AuthTokenError(e)

    def _encode(
            self,
            sub: str,
    ) -> str:
        current_timestamp = int(time())
        claims = {
            'sub': sub,
            'exp': current_timestamp + self._auth_token_ttl,
            'iat': current_timestamp,
        }

        try:
            return jwt.encode(claims, self._auth_secret_key, algorithm=self._algorithms)
        except JWTError as e:
            raise AuthTokenError(e)

    def generate_token(self, sub: str) -> TokenStruct:
        return TokenStruct(
            access_token=self._encode(
                sub=str(sub)
            ),
            token_type='bearer'
        )

    def get_user_info_from_token(self, token: str) -> AuthTokenUserInfoStruct:
        data = self._decode(token)
        return AuthTokenUserInfoStruct(
            user_id=data.sub
        )
