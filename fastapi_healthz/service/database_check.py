try:
    from sqlalchemy import create_engine, text
    from sqlalchemy.orm import sessionmaker
except ImportError:
    create_engine = None
    text = None
    sessionmaker = None

from .abstract import HealthCheckAbstract
from ..models import HealthCheckStatusEnum


class HealthCheckDatabase(HealthCheckAbstract):
    def __init__(self, uri: str):
        self.__uri = uri

    @property
    def service(self) -> str:
        return "db"

    @property
    def connection_uri(self) -> str | None:
        return self.__uri

    @property
    def tags(self) -> list[str]:
        return ["database"]

    @property
    def comments(self) -> list[str]:
        return []

    def check_health(self) -> HealthCheckStatusEnum:
        if create_engine is None or text is None or sessionmaker is None:
            raise ImportError("SQLAlchemy is not installed. Install it with `pip install fastapi-healthz[database]`.")

        res: HealthCheckStatusEnum = HealthCheckStatusEnum.UNHEALTHY

        engine = create_engine(self.__uri)
        Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        with Session() as session:
            try:
                session.execute(text("SELECT 1"))
                res = HealthCheckStatusEnum.HEALTHY
            except Exception:
                pass
        return res
