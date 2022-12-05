from pydantic import BaseModel
from pydantic import Field
from pydantic import validator

from src.value_object.value_object import PostTitle
from src.value_object.value_object import PostDescription


class CreatePostRequest(BaseModel):
    title: str = Field(..., min_length=3, max_length=30)
    description: str = Field(..., min_length=3, max_length=250)

    @validator('title')
    def title_format(cls, title: str) -> str:
        return str(PostTitle(title))

    @validator('description')
    def description_format(cls, description: str) -> str:
        return str(PostDescription(description))
