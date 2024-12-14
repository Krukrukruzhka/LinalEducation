import os

from typing import Optional
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    host: str = Field(
        default=os.getenv("LINAL_HOST", "::"),
        description="Host to run on",
        json_schema_extra={"type": str}
    )
    port: int = Field(
        default=int(os.getenv("LINAL_PORT", 8001)),
        description="Port to run on",
        json_schema_extra={"type": int}
    )
    mode: str = Field(
        default=os.getenv("APPLICATION_ENV", "LOCAL"),
        description="application environment",
        json_schema_extra={"type": str},
    )
    workers: int = Field(
        default=1,
        description="Number of workers",
        json_schema_extra={"type": int}
    )
    worker_class: str = Field(
        default="uvicorn.workers.UvicornWorker",
        description="Worker class",
        json_schema_extra={"type": str}
    )
    worker_timeout: int = Field(
        default=300,
        description="Worker timeout",
        json_schema_extra={"type": int}
    )
    routes_timeout: int = Field(
        default=60,
        description="FastAPI route timeout",
        json_schema_extra={"type": int}
    )
    max_requests: int = Field(
        default=100,
        description="The maximum number of requests a worker will process before restarting.",
        json_schema_extra={"type": int, 'required': True},
    )
    log_path: str = Field(
        default="/linal_logs/",
        description="Path to log dir",
        json_schema_extra={"type": str}
    )
    template_path: str = Field(
        default="/linal_templates/",
        description="Path to templates dir",
        json_schema_extra={"type": str}
    )
