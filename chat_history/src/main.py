from logging.config import dictConfig
from fastapi import FastAPI

from api.api import api_router
from config.logger import get_app_logger
from config.settings import settings, LOGGING


dictConfig(LOGGING)
logger = get_app_logger()


app = FastAPI(
    title='Telegram Chat History API',
    openapi_url=f'{settings.API_V1}/openapi.json',
)

app.include_router(api_router, prefix=settings.API_V1)
