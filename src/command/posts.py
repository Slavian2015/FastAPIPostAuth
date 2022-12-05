from pydantic import BaseModel


class CreatePostCommand(BaseModel):
    title: str
    description: str
    user_id: str
