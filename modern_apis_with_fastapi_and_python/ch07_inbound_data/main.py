import asyncio
from services import openweather_service
from starlette.staticfiles import StaticFiles
from api import weather_api
from views import home
from pathlib2 import Path
from models.location import Location
from services import report_service
import uvicorn
import fastapi
import json

api = fastapi.FastAPI()


def configure():
    configure_routing()
    configure_api_keys()
    configure_fake_data()


def configure_api_keys():
    file = Path("settings.json").absolute()
    if not file.exists():
        print(
            f"WARNING: {file} file not found, you cannot continue, please see settings_template.json"
        )
        raise Exception(
            "settings.json file not found, you cannot continue, please see settings_template.json"
        )

    with open("settings.json") as fin:
        settings = json.load(fin)
        openweather_service.api_key = settings.get("api_key")


def configure_routing():
    api.mount("/static", StaticFiles(directory="static"))
    api.include_router(home.router)
    api.include_router(weather_api.router)


def configure_fake_data():
    # This was added to make it easier to test the weather event reporting
    # We have /api/reports but until you submit new data each run, it's missing
    # So this will give us something to start from.
    loop = None
    try:
        loop = asyncio.get_running_loop()
        print("got loop!", loop)
    except RuntimeError:
        pass  # Boo, why can't I just get nothing back?

    if not loop:
        loop = asyncio.get_event_loop()

    try:
        loc = Location(city="Portland", state="OR", country="US")
        loop.run_until_complete(
            report_service.add_report("Misty sunrise today, beautiful!", loc)
        )
        loop.run_until_complete(report_service.add_report("Clouds over downtown.", loc))
    except RuntimeError:
        print(
            "Note: Could not import starter date, this fails on some systems and "
            "some ways of running the app under uvicorn."
        )
        print("Fake starter data will no appear on home page.")
        print("Once you add data with the client, it will appear properly.")


if __name__ == "__main__":
    configure()
    uvicorn.run("main:api", port=8000, host="127.0.0.1", reload=True)  #
else:
    configure()
