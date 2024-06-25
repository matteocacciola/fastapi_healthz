from typing import Any
from pymongo import MongoClient

from .abstract import HealthCheckAbstract
from ..models import HealthCheckStatusEnum


class HealthCheckMongoDb(HealthCheckAbstract):
    def __init__(self, uri: str, service: str | None = None, tags: list[str] | None = None, **kwargs: Any):
        super().__init__(service=service, tags=tags)

        self.__uri = uri
        self.__kwargs = kwargs

    @property
    def service(self) -> str:
        return self._service if self._service is not None else "mongodb"

    @property
    def connection_uri(self) -> str | None:
        return self.__uri

    def check_health(self) -> HealthCheckStatusEnum:
        res: HealthCheckStatusEnum = HealthCheckStatusEnum.UNHEALTHY

        try:
            client = MongoClient(**self.__kwargs)
            client.server_info()
            res = HealthCheckStatusEnum.HEALTHY
        except Exception:
            pass

        return res
