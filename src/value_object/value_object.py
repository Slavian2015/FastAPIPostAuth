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


class PostTitle:
    def __init__(self, title: str) -> None:
        valid_name = r"^[a-zA-Z0-9-( )_]*$"
        valid_first_character = r"^[a-zA-Z]*$"
        if not title:
            raise ValueError('Invalid post name')

        if not re.match(valid_name, title):
            raise ValueError('Invalid post title.'
                             'Valid post name can only contain alphanumeric characters and underscores')
        if not re.match(valid_first_character, title[0]):
            raise ValueError('Invalid post title. '
                             'The first character of valid post title must be an alphabetic character')
        self._title = title

    def __str__(self) -> str:
        return self._title


class PostDescription:
    def __init__(self, description: str) -> None:
        valid_name = r"^[a-zA-Z0-9-( )_.]*$"
        if not description:
            raise ValueError('Invalid post description')
        if not re.match(valid_name, description):
            raise ValueError('Invalid post description.'
                             'Valid post name can only contain alphanumeric characters and underscores')
        self._description = description

    def __str__(self) -> str:
        return self._description
