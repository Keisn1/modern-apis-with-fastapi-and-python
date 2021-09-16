from services import openweather_service
from models.location import Location
from typing import Optional
from fastapi import Depends

import fastapi

router = fastapi.APIRouter()


@router.get("/api/weather/{city}")
async def weather(
    loc: Location = Depends(), units: Optional[str] = "metric"
):  # pydantic models only come from http post of bodies, therefore use Depends

    report = await openweather_service.get_report_async(
        loc.city, loc.state, loc.country, units
    )  # report is now a coroutine
    print(type(report), report)

    return report
