from __future__ import annotations

import datetime
from typing import Optional

from pydantic import BaseModel


class AnalyticsCardResponse(BaseModel):
    date: datetime.date
    qty: int


class GetAnalyticsDetailsResponse(BaseModel):
    likes: list[AnalyticsCardResponse]


class GetActivityDetailsResponse(BaseModel):
    last_login:  datetime.date
    last_request:  Optional[datetime.date]
