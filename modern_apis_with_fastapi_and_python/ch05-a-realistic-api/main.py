import fastapi
from starlette.requests import Request
import uvicorn
from starlette.templating import Jinja2Templates

api = fastapi.FastAPI()
templates = Jinja2Templates("templates")


@api.get("/")
def index(request: Request):
    return templates.TemplateResponse("home/index.html", {"request": request})


if __name__ == "__main__":
    uvicorn.run("main:api", port=8000, host="127.0.0.1", reload=True)
