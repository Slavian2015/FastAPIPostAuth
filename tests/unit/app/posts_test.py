import pytest
from src.api.posts.request import CreatePostRequest


@pytest.mark.parametrize('title', [('qweasdzx:c',), ('123qweasd',), ('QQ',)])
def test_invalid_title_raise_error(title: str) -> None:
    with pytest.raises(ValueError):
        CreatePostRequest(title=title, description="Description")


def test_valid_password_returned() -> None:
    req = CreatePostRequest(title="Title", description="Description")
    assert req.title == 'Title'
