try:
    import boto3
    from sqlalchemy.orm import sessionmaker
except ImportError:
    boto3 = None

from .abstract import HealthCheckAbstract
from ..models import HealthCheckStatusEnum


class HealthCheckS3(HealthCheckAbstract):
    def __init__(self, endpoint: str, access_key: str, secret_key: str):
        self._endpoint = endpoint
        self._access_key = access_key
        self._secret_key = secret_key

    @property
    def service(self) -> str:
        return "s3"

    @property
    def connection_uri(self) -> str | None:
        return self._endpoint

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
                endpoint_url=self._endpoint,
                aws_access_key_id=self._access_key,
                aws_secret_access_key=self._secret_key,
            )
            s3_client.list_buckets()
            res = HealthCheckStatusEnum.HEALTHY
        except Exception:
            pass

        return res
