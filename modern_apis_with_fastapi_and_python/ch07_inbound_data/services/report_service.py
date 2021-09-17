from datetime import datetime
import uuid
from models.reports import Report
from models.location import Location
from typing import List, Optional

__reports: List[Report] = []


async def get_reports() -> List[Report]:
    # needs to be asynchronous
    # would be an async call here
    return list(__reports)


async def add_report(description: str, location: Optional[Location] = None) -> Report:
    now = datetime.now()
    report = Report(
        id=str(uuid.uuid4()),
        location=location,
        description=description,
        created_date=now,
    )
    # simulate saving to the DataBase
    __reports.append(report)

    __reports.sort(key=lambda r: r.created_date, reverse=True)
    return report
