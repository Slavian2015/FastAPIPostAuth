import datetime

from pydantic import BaseModel


class GetAnalyticsQuery(BaseModel):
    date_from: datetime.date
    date_to: datetime.date
