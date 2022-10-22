import logging
from typing import Any

from pydantic import BaseSettings, PostgresDsn

# from app.core.logging import InterceptHandler


class BaseAppSettings(BaseSettings):
    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


class AppSettings(BaseAppSettings):
    debug: bool = False
    docs_url: str = "/docs"
    openapi_prefix: str = ""
    openapi_url: str = "/openapi.json"
    redoc_url: str = "/redoc"
    title: str = "Secure_T test task"
    version: str = "1.0.0"

    database_url: PostgresDsn

    server_host: str = "127.0.0.1"
    server_port: int = 8000

    jwt_secret: str
    jwt_algorithm: str = "HS256"
    jwt_expiration: int = 3600

    logging_level: int = logging.INFO
    loggers: tuple[str, str] = ("uvicorn.asgi", "uvicorn.access")

    @property
    def fastapi_kwargs(self) -> dict[str, Any]:
        return {
            "debug": self.debug,
            "docs_url": self.docs_url,
            "openapi_prefix": self.openapi_prefix,
            "openapi_url": self.openapi_url,
            "redoc_url": self.redoc_url,
            "title": self.title,
            "version": self.version,
        }

    # def configure_logging(self) -> None:
    #     logging.getLogger().handlers = [InterceptHandler()]
    #     for logger_name in self.loggers:
    #         logging_logger = logging.getLogger(logger_name)
    #         logging_logger.handlers = [InterceptHandler(level=self.logging_level)]
    #
    #     logger.configure(handlers=[{"sink": sys.stderr, "level": self.logging_level}])


settings = AppSettings()
