from pydantic import BaseModel


class GetUserDetailsQuery(BaseModel):
    user_id: str
