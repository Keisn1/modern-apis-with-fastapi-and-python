from models.validation_error import ValidationError
from httpx import Response
from infrastructure.weather_cache import get_weather, set_weather
from typing import Optional, Tuple
import httpx

api_key: Optional[str] = None


async def get_report_async(
    city: str, state: Optional[str], country: Optional[str], units: Optional[str]
) -> dict:
    city, state, country, units = validate_units(city, state, country, units)

    if forecast := get_weather(city, state, country, units):
        return forecast

    if state is not None:
        q = f"{city},{state},{country}"
    else:
        q = f"{city}, {country}"
    url = f"https://api.openweathermap.org/data/2.5/weather?q={q}&appid={api_key}&units={units}"

    async with httpx.AsyncClient() as client:
        resp: Response = await client.get(url)
        if resp.status_code != 200:
            raise ValidationError(resp.text, status_code=resp.status_code)

    data = resp.json()
    forecast = data["main"]

    set_weather(city, state, country, units, forecast)

    return forecast


def validate_units(
    city: str, state: Optional[str], country: Optional[str], units: Optional[str]
) -> Tuple[str, Optional[str], Optional[str], Optional[str]]:
    city = city.lower().strip()
    if not country:
        country = "us"
    else:
        country = country.lower().strip()

    if len(country) != 2:
        error = f"Invalid country: {country}. It must be a two letter abbreviation such as US or GB."
        raise ValidationError(status_code=400, error_msg=error)

    if state:
        state = state.strip().lower()

    if state and len(state) != 2:
        error = f"Invalid state: {state}. It must be a two letter abbreviation such as CA or KS (use for US only)."
        raise ValidationError(status_code=400, error_msg=error)

    if units:
        units = units.strip().lower()

    valid_units = {"standard", "metric", "imperial"}
    if units not in valid_units:
        error = f"Invalid units '{units}', it must be one of {valid_units}."
        raise ValidationError(status_code=400, error_msg=error)

    return city, state, country, units
