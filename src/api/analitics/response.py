from __future__ import annotations

import datetime
from pydantic import BaseModel


class AnalyticsCardResponse(BaseModel):
    date: datetime.date
    qty: int


class GetAnalyticsDetailsResponse(BaseModel):
    likes: list[AnalyticsCardResponse]
