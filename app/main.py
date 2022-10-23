from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException
from starlette.middleware.cors import CORSMiddleware

from app.core.settings import settings
from app.api.routes.api import router as api_router


def get_application() -> FastAPI:

    # settings.configure_logging()

    application = FastAPI(**settings.fastapi_kwargs)

    application.include_router(api_router, prefix=settings.api_prefix)
    return application


app = get_application()
