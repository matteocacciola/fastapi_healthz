from datetime import timedelta
from typing import Any
from pydantic import BaseModel, Field, field_serializer

from .utils import Enum as BaseEnum


class HealthCheckStatusEnum(BaseEnum):
    HEALTHY = "healthy"
    UNHEALTHY = "unhealthy"


class HealthCheckEntityModel(BaseModel):
    service: str
    status: str = Field(default=str(HealthCheckStatusEnum.HEALTHY))
    time_taken: timedelta = Field(default=timedelta())
    tags: list[str] = Field(default_factory=list)
    comments: list[str] = Field(default_factory=list)

    @field_serializer("time_taken")
    def serialize_time_taken(self, time: timedelta) -> str:
        # Pydantic will now call this to serialize the timedelta field
        return str(time)


class HealthCheckModel(BaseModel):
    status: str = Field(default=str(HealthCheckStatusEnum.HEALTHY))
    total_time_taken: timedelta = Field(default=timedelta())
    entities: list[dict[str, Any]] = Field(default_factory=list)

    @field_serializer("total_time_taken")
    def serialize_total_time_taken(self, time: timedelta) -> str:
        # Pydantic will now call this to serialize the timedelta field
        return str(time)
