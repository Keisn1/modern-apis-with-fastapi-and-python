import sys
from typing import Optional

from starlette.responses import JSONResponse

print(sys.path)
import fastapi

# import uvicorn

api = fastapi.FastAPI()


@api.get("/")
def index():
    body = (
        "<html>"
        "<body style='padding: 10px;'>"
        "<h1>Welcome to the API</h1>"
        "<div>"
        "Try it: <a href='/api/calculate?x=7&y=11'>/api/calculate?x=7&y=11</a>"
        "</div>"
        "</body>"
        "</html"
    )

    return fastapi.responses.HTMLResponse(content=body)


@api.get("/api/calculate")
def calculate(x: int, y: int, z: Optional[int] = None) -> JSONResponse:  # using pypint

    if z is not None and z == 0:
        return fastapi.responses.JSONResponse(
            content={"error": "ERROR: Z cannot be zero."}, status_code=400
        )

    result = x + y

    if z is not None:
        result /= z

    return JSONResponse({"x": x, "y": y, "z": z, "result": result})


# uvicorn.run(api)
