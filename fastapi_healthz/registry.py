from datetime import datetime, timedelta

from .models import HealthCheckStatusEnum, HealthCheckModel, HealthCheckEntityModel
from .service import HealthCheckAbstract


class HealthCheckRegistry:
    def __init__(self) -> None:
        self.__health_items: list[HealthCheckAbstract] = []
        self.__health: HealthCheckModel | None = None
        self.__entity_start_time: datetime | None = None
        self.__entity_stop_time: datetime | None = None
        self.__total_start_time: datetime | None = None
        self.__total_stop_time: datetime | None = None

    def add(self, item: HealthCheckAbstract) -> None:
        self.__health_items.append(item)

    def add_many(self, items: list[HealthCheckAbstract]) -> None:
        self.__health_items.extend(items)

    def __start_timer(self, entity_timer: bool) -> None:
        if entity_timer:
            self.__entity_start_time = datetime.now()
        else:
            self.__total_start_time = datetime.now()

    def __stop_timer(self, entity_timer: bool) -> None:
        if entity_timer:
            self.__entity_stop_time = datetime.now()
        else:
            self.__total_stop_time = datetime.now()

    def __get_time_taken(self, entity_timer: bool) -> timedelta:
        if entity_timer:
            return self.__entity_stop_time - self.__entity_start_time
        return self.__total_stop_time - self.__total_start_time

    def check(self) -> dict:
        self.__health = HealthCheckModel()
        self.__start_timer(False)
        for i in self.__health_items:
            # Generate the model
            item = HealthCheckEntityModel(service=i.service, tags=i.tags, comments=i.comments)

            # Track how long the entity took to respond
            self.__start_timer(True)
            item.status = str(i.check_health())
            self.__stop_timer(True)
            item.time_taken = self.__get_time_taken(True)

            # if we have one dependency unhealthy, the service in unhealthy
            if item.status == HealthCheckStatusEnum.UNHEALTHY:
                self.__health.status = str(HealthCheckStatusEnum.UNHEALTHY)

            self.__health.entities.append(item.model_dump(mode="json"))
        self.__stop_timer(False)
        self.__health.total_time_taken = self.__get_time_taken(False)

        return self.__health.model_dump(mode="json")
