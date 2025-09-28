from typing import Any
try:
    from pymongo import MongoClient
except ImportError:
    MongoClient = None

from .abstract import HealthCheckAbstract
from ..models import HealthCheckStatusEnum


class HealthCheckMongoDb(HealthCheckAbstract):
    def __init__(self, host: str | None, port: str | None, **kwargs: Any):
        self.__host = host
        self.__port = port
        self.__kwargs = kwargs

    @property
    def service(self) -> str:
        return "mongodb"

    @property
    def connection_uri(self) -> str | None:
        return f"mongodb://{self.__host}:{self.__port}" if self.__host and self.__port else None

    @property
    def tags(self) -> list[str]:
        return ["mongodb", "database"]

    @property
    def comments(self) -> list[str]:
        return []

    def check_health(self) -> HealthCheckStatusEnum:
        if MongoClient is None:
            raise ImportError("pymongo is not installed. Install it with `pip install fastapi-healthz[mongodb]`.")

        res: HealthCheckStatusEnum = HealthCheckStatusEnum.UNHEALTHY

        try:
            client = MongoClient(host=self.__host, port=self.__port, **self.__kwargs)
            client.server_info()
            res = HealthCheckStatusEnum.HEALTHY
        except Exception:
            pass

        return res
