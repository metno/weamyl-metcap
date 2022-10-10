from pathlib import Path

from fastapi import FastAPI, APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi


from app.api.api_v1.api import api_router
from app.core.config import settings



BASE_PATH = Path(__file__).resolve().parent
TEMPLATES = Jinja2Templates(directory=str(BASE_PATH / "templates"))


root_router = APIRouter()
app = FastAPI(title="MAP API",
              docs_url="/api/docs",
              openapi_url="/api/openapi.json")


origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def my_schema():
    openapi_schema = get_openapi(
        title="METNO METCAP API",
        version="1.0",
        routes=app.routes,
        )
    openapi_schema["info"] = {
        "title": "METNO METCAP API",
        "version": "1.0",
        "description": "METNO METCAP API",
        "termsOfService": "TBD",
        "contact": {
            "name": "Get Help with this API",
            "url": "TBD",
            "email": "TBD"
            },
        "license": {
            "name": "Apache 2.0",
            "url": "https://www.apache.org/licenses/LICENSE-2.0.html"
            },
        }
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = my_schema


# @app.middleware("http")
# async def add_process_time_header(request: Request, call_next):
#     start_time = time.time()
#     response = await call_next(request)
#     process_time = time.time() - start_time
#     response.headers["X-Process-Time"] = str(process_time)
#     return response


app.include_router(api_router, prefix=settings.API_V1_STR)
app.include_router(root_router)


if __name__ == "__main__":
    # Use this for debugging purposes only
    import uvicorn

    uvicorn.run(app, host="localhost", port=7532, log_level="debug")
