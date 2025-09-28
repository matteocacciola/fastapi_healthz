from abc import ABC, abstractmethod
from ..models import HealthCheckStatusEnum


class HealthCheckAbstract(ABC):
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
    @abstractmethod
    def tags(self) -> list[str]:
        pass

    @property
    @abstractmethod
    def comments(self) -> list[str]:
        pass
