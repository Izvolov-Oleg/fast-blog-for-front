from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException

from app.api.errors.http_error import http_error_handler
from app.api.errors.validation_error import http422_error_handler
from app.core.settings import settings
from app.api.routes.api import router as api_router


def get_application() -> FastAPI:

    settings.configure_logging()

    application = FastAPI(**settings.fastapi_kwargs)

    application.add_exception_handler(HTTPException, http_error_handler)
    application.add_exception_handler(RequestValidationError, http422_error_handler)

    application.include_router(api_router, prefix=settings.api_prefix)
    return application


app = get_application()
