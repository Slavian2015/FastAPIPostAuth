import re
import validators


class PlainPassword:
    def __init__(self, password: str) -> None:
        valid_password = r'^(?=.*[a-z])(?=.*[A-Z]).{8,}$'
        if not re.match(valid_password, password):
            raise ValueError('Invalid password. '
                             'Valid password must be at least 8 characters long and contain '
                             'both lower and uppercase characters '
                             'and at least one number')
        self._password = password

    def __str__(self) -> str:
        return self._password


class Email:
    def __init__(self, email: str) -> None:
        if not validators.email(email):
            raise ValueError('Invalid emails')
        self._email = email

    def __str__(self) -> str:
        return self._email
