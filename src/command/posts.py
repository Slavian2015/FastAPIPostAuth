from pydantic import BaseModel


class CreatePostCommand(BaseModel):
    title: str
    description: str
    user_id: str


class LikePostCommand(BaseModel):
    post_id: str
    user_id: str


class UnLikePostCommand(BaseModel):
    post_id: str
    user_id: str
