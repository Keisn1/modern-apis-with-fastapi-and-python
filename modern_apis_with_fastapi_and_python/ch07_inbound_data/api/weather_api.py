from models.reports import Report, ReportSubmittal
from models.validation_error import ValidationError
from services import openweather_service, report_service
from models.location import Location
from typing import List, Optional
from fastapi import Depends

import fastapi

router = fastapi.APIRouter()


@router.get("/api/weather/{city}")
async def weather(
    loc: Location = Depends(), units: Optional[str] = "metric"
):  # pydantic models only come from http post of bodies, therefore use Depends

    try:
        return await openweather_service.get_report_async(
            loc.city, loc.state, loc.country, units
        )  # report is now a coroutine
    except ValidationError as ve:
        return fastapi.Response(content=ve.error_msg, status_code=ve.status_code)
    except Exception as x:
        return fastapi.Response(content=str(x), status_code=500)


@router.get("/api/reports", name="all_reports")
async def reports_get() -> List[Report]:
    return await report_service.get_reports()


@router.post("/api/reports", name="add_reports", status_code=201)
async def reports_post(report_submittel: ReportSubmittal) -> Report:
    d = report_submittel.description
    loc = report_submittel.location

    return await report_service.add_report(d, loc)
