from abc import ABC, abstractmethod
from ..models import HealthCheckStatusEnum


class HealthCheckAbstract(ABC):
    def __init__(self, service: str | None = None, tags: list[str] | None = None):
        self._service = service
        self._tags = tags

    @abstractmethod
    def check_health(self) -> HealthCheckStatusEnum:
        """Requests data from the endpoint to validate health."""
        pass

    @property
    @abstractmethod
    def service(self) -> str:
        pass

    @property
    @abstractmethod
    def connection_uri(self) -> str | None:
        pass

    @property
    def tags(self) -> list[str]:
        if self._tags:
            return self._tags
        if self.service:
            return [self.service]
        return []