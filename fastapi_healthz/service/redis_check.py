try:
    from redis import Redis
except ImportError:
    Redis = None

from .abstract import HealthCheckAbstract
from ..models import HealthCheckStatusEnum
from ..utils import run_sync_async


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
        if Redis is None:
            raise ImportError("redis is not installed. Install it with `pip install fastapi-healthz[redis]`.")

        res: HealthCheckStatusEnum = HealthCheckStatusEnum.UNHEALTHY
        try:
            db = Redis.from_url(self.__uri, socket_connect_timeout=5, socket_timeout=5)

            status = run_sync_async(db.ping)
            if status:
                res = HealthCheckStatusEnum.HEALTHY
        except Exception:
            pass

        return res
