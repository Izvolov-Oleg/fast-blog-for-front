from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException
from starlette.middleware.cors import CORSMiddleware

from app.core.settings import settings


def get_application() -> FastAPI:

    # settings.configure_logging()

    application = FastAPI(**settings.fastapi_kwargs)

    return application


app = get_application()
