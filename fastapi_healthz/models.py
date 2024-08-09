from datetime import timedelta
from enum import Enum as BaseEnum
from pydantic import BaseModel


class HealthCheckStatusEnum(BaseEnum):
    def __str__(self):
        return str(self.value)

    HEALTHY = "Healthy"
    UNHEALTHY = "Unhealthy"


class HealthCheckEntityModel(BaseModel):
    service: str
    status: HealthCheckStatusEnum = HealthCheckStatusEnum.HEALTHY
    time_taken: timedelta | None = None
    tags: list[str] = []


class HealthCheckModel(BaseModel):
    status: HealthCheckStatusEnum = HealthCheckStatusEnum.HEALTHY
    total_time_taken: timedelta | None = None
    entities: list[HealthCheckEntityModel] = []
