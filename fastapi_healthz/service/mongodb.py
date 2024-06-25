from typing import Any
from pymongo import MongoClient

from .abstract import HealthCheckAbstract
from ..models import HealthCheckStatusEnum


class HealthCheckMongoDb(HealthCheckAbstract):
    def __init__(
        self,
        host: str | None,
        port: str | None,
        service: str | None = None,
        tags: list[str] | None = None,
        **kwargs: Any
    ):
        super().__init__(service=service, tags=tags)

        self.__host = host
        self.__port = port
        self.__kwargs = kwargs

    @property
    def service(self) -> str:
        return self._service if self._service is not None else "mongodb"

    @property
    def connection_uri(self) -> str | None:
        return f"mongodb://{self.__host}:{self.__port}" if self.__host and self.__port else None

    def check_health(self) -> HealthCheckStatusEnum:
        res: HealthCheckStatusEnum = HealthCheckStatusEnum.UNHEALTHY

        try:
            client = MongoClient(host=self.__host, port=self.__port, **self.__kwargs)
            client.server_info()
            res = HealthCheckStatusEnum.HEALTHY
        except Exception:
            pass

        return res
