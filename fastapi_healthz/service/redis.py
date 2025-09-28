import asyncio
import time
import random
try:
    import aioredis
except ImportError:
    aioredis = None

from .abstract import HealthCheckAbstract
from ..models import HealthCheckStatusEnum


class HealthCheckRedis(HealthCheckAbstract):
    def __init__(self, uri: str):
        self.__uri = uri

    @property
    def service(self) -> str:
        return "redis"

    @property
    def connection_uri(self) -> str | None:
        return self.__uri

    @property
    def tags(self) -> list[str]:
        return ["redis", "cache", "database"]

    @property
    def comments(self) -> list[str]:
        return []

    def check_health(self) -> HealthCheckStatusEnum:
        if aioredis is None:
            raise ImportError("aioredis is not installed. Install it with `pip install fastapi-healthz[redis]`.")

        res: HealthCheckStatusEnum = HealthCheckStatusEnum.UNHEALTHY

        try:
            redis = aioredis.from_url(self.__uri)
            test_key = 'health_check_' + str(random.random()) + str(time.time())

            asyncio.run(redis.set(test_key, 'value'))
            result = asyncio.run(redis.get(test_key))

            asyncio.run(redis.delete(test_key))
            status = result == 'value'
            redis.close()
            asyncio.run(redis.wait_closed())

            if status:
                res = HealthCheckStatusEnum.HEALTHY
        except Exception:
            pass

        return res
