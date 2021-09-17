import datetime
from typing import Optional

from models.location import Location
from pydantic.main import BaseModel


class ReportSubmittal(BaseModel):
    description: str
    location: Location


class Report(ReportSubmittal):
    id: str
    created_date: Optional[datetime.datetime]
