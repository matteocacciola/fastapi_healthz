from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from .abstract import HealthCheckAbstract
from ..models import HealthCheckStatusEnum


class HealthCheckSQLAlchemy(HealthCheckAbstract):
    def __init__(
        self,
        driver: str,
        username: str,
        password: str,
        host: str,
        database: str,
        port: int | None = 3306,
        tags: list[str] | None = None
    ):
        super().__init__(tags=tags)

        self.__uri = f"{driver}://{username}:{password}@{host}:{port}/{database}"

    @property
    def service(self) -> str:
        return "db"

    @property
    def connection_uri(self) -> str | None:
        return self.__uri

    def check_health(self) -> HealthCheckStatusEnum:
        res: HealthCheckStatusEnum = HealthCheckStatusEnum.UNHEALTHY

        engine = create_engine(self.__uri)
        with sessionmaker(autocommit=False, autoflush=False, bind=engine) as session:
            try:
                session.execute(text("SELECT 1"))
                res = HealthCheckStatusEnum.HEALTHY
            except Exception:
                pass
        return res
