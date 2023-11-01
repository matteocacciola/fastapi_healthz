from requests import get
from ..models import HealthCheckStatusEnum
from .abstract import HealthCheckAbstract


class HealthCheckUri(HealthCheckAbstract):
    def __init__(
        self,
        uri: str,
        service: str | None = None,
        tags: list[str] | None = None,
        healthy_code: int = 200,
        unhealthy_code: int = 500
    ) -> None:
        super().__init__(service=service, tags=tags)

        self.__connection_uri = uri
        self.__healthy_code = healthy_code
        self.__unhealthy_code = unhealthy_code

    @property
    def service(self) -> str:
        return self._service if self._service is not None else "uri"

    @property
    def connection_uri(self) -> str | None:
        return self.__connection_uri

    def check_health(self) -> HealthCheckStatusEnum:
        res = get(url=self.__connection_uri, headers={"User-Agent": "FastAPI HealthCheck"})
        if res.status_code == self.__healthy_code:
            return HealthCheckStatusEnum.HEALTHY
        elif res.status_code != self.__unhealthy_code:
            return HealthCheckStatusEnum.UNHEALTHY
        return HealthCheckStatusEnum.UNHEALTHY
