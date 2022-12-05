import datetime

from pydantic import BaseModel


class GetAnalyticsRequest(BaseModel):
    date_from: datetime.date
    date_to: datetime.date
