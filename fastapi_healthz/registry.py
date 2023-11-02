from datetime import datetime, timedelta
from .models import HealthCheckStatusEnum, HealthCheckModel, HealthCheckEntityModel
from .service import HealthCheckAbstract


class HealthCheckRegistry:
    def __init__(self) -> None:
        self.__health_items: list[HealthCheckAbstract] = list()
        self.__health: HealthCheckModel | None = None
        self.__entity_start_time: datetime | None = None
        self.__entity_stop_time: datetime | None = None
        self.__total_start_time: datetime | None = None
        self.__total_stop_time: datetime | None = None

    def add(self, item: HealthCheckAbstract) -> None:
        self.__health_items.append(item)

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

    def __dump_model(self) -> dict:
        """
        This goes and convert python objects to something a json object.
        """

        def fnc(x: HealthCheckEntityModel) -> HealthCheckEntityModel:
            y = dict(x)
            y["status"] = x.status.value
            y["time_taken"] = str(x.time_taken)
            return y

        self.__health.entities = [fnc(i) for i in self.__health.entities]
        self.__health.status = str(self.__health.status)
        self.__health.total_time_taken = str(self.__health.total_time_taken)

        return dict(self.__health)

    def check(self) -> dict:
        self.__health = HealthCheckModel()
        self.__start_timer(False)
        for i in self.__health_items:
            # Generate the model
            item = HealthCheckEntityModel(service=i.service, tags=i.tags)

            # Track how long the entity took to respond
            self.__start_timer(True)
            item.status = i.check_health()
            self.__stop_timer(True)
            item.time_taken = self.__get_time_taken(True)

            # if we have one dependency unhealthy, the service in unhealthy
            if item.status == HealthCheckStatusEnum.UNHEALTHY:
                self.__health.status = HealthCheckStatusEnum.UNHEALTHY

            self.__health.entities.append(item)
        self.__stop_timer(False)
        self.__health.total_time_taken = self.__get_time_taken(False)

        return self.__dump_model()
