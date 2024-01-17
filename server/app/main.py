import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from routers.api import main as api_main
from routers.wellknown import main as wellknown_main
from routers.nodeinfo import main as nodeinfo_main
from util.env import get_env

# logger config
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(level=logging.DEBUG)

# get environment mode
env_mode = get_env("ENV_MODE", "development")

# production時，docsを表示しない
app_params = {}
if env_mode == "production":
    app_params["docs_url"] = None
    app_params["redoc_url"] = None
    app_params["openapi_url"] = None

# create app
app = FastAPI(**app_params)

origins = [
    "http://b02.isp2.ukwhatn.com",
    "https://b02.isp2.ukwhatn.com",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# mount static folder
app.mount("/static", StaticFiles(directory="/app/static"), name="static")

# add routers
app.include_router(
    api_main.router,
    prefix="/api"
)

app.include_router(
    wellknown_main.router,
    prefix="/.well-known"
)

app.include_router(
    nodeinfo_main.router,
    prefix="/nodeinfo"
)