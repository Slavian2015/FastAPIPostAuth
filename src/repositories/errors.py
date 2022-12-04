class RepositoryError(RuntimeError):
    message: str = ''

    def __init__(self) -> None:
        super().__init__(self.message)


class PersistenceError(RuntimeError):
    pass


class UserExistsError(RuntimeError):
    pass


class PostExistsError(RuntimeError):
    pass


class PostNotExistsError(RepositoryError):
    message = 'Post not found'


class UserNotExistsError(RepositoryError):
    message = 'User not found'
