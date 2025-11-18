try:
    import boto3
    from sqlalchemy.orm import sessionmaker
except ImportError:
    boto3 = None

from .abstract import HealthCheckAbstract
from ..models import HealthCheckStatusEnum


class HealthCheckS3(HealthCheckAbstract):
    def __init__(self, endpoint: str, access_key: str, secret_key: str, ssl: bool):
        self.__endpoint = endpoint
        self.__access_key = access_key
        self.__secret_key = secret_key
        self.__ssl = ssl

    @property
    def service(self) -> str:
        return "s3"

    @property
    def connection_uri(self) -> str | None:
        return self.__endpoint

    @property
    def tags(self) -> list[str]:
        return ["s3"]

    @property
    def comments(self) -> list[str]:
        return []

    def check_health(self) -> HealthCheckStatusEnum:
        if boto3 is None:
            raise ImportError("boto3 is not installed. Install it with `pip install fastapi-healthz[s3]`.")

        res: HealthCheckStatusEnum = HealthCheckStatusEnum.UNHEALTHY

        try:
            s3_client = boto3.client(
                "s3",
                endpoint_url=self.__endpoint,
                aws_access_key_id=self.__access_key,
                aws_secret_access_key=self.__secret_key,
                verify=self.__ssl,
            )
            s3_client.list_buckets()
            res = HealthCheckStatusEnum.HEALTHY
        except Exception:
            pass

        return res
