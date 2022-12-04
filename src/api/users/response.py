from __future__ import annotations

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel

from src.domain.users import User


class UpdateUserResponse(BaseModel):
    status: str = 'OK'


class DeleteUserResponse(BaseModel):
    status: str = 'OK'


class GetUserDetailsResponse(BaseModel):
    id: UUID
    email: str
    date_created: datetime
    date_updated: Optional[datetime]
    date_deleted: Optional[datetime]
    date_logged: datetime

    @staticmethod
    def from_data(user: User) -> GetUserDetailsResponse:
        return GetUserDetailsResponse(
            id=user.id,
            email=user.email,
            date_created=user.date_created,
            date_updated=user.date_updated,
            date_deleted=user.date_deleted,
            date_logged=user.date_logged,
        )
