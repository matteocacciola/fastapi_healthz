from ssl import SSLContext, PROTOCOL_TLSv1_2
import pika
from .abstract import HealthCheckAbstract
from ..models import HealthCheckStatusEnum


class HealthCheckRabbitMQ(HealthCheckAbstract):
    def __init__(
        self,
        host: str,
        vhost: str,
        username: str,
        password: str,
        ssl: bool = True,
        port: int | None = 5672,
        service: str | None = None,
        tags: list[str] | None = None
    ):
        super().__init__(service=service, tags=tags)

        self.__host = host
        self.__port = port
        self.__vhost = vhost
        self.__username = username
        self.__password = password
        self.__ssl = ssl

    @property
    def service(self) -> str:
        return self._service if self._service is not None else "rabbitmq"

    @property
    def connection_uri(self) -> str | None:
        return f"amqp://{self.__username}:{self.__password}@{self.__host}:{str(self.__port)}"

    def check_health(self) -> HealthCheckStatusEnum:
        res: HealthCheckStatusEnum = HealthCheckStatusEnum.UNHEALTHY
        try:
            parameters = pika.ConnectionParameters(
                host=self.__host,
                port=self.__port,
                virtual_host=self.__vhost,
                credentials=pika.PlainCredentials(username=self.__username, password=self.__password),
            )

            if self.__ssl:
                # SSL Context for TLS configuration of Amazon MQ for RabbitMQ
                ssl_context = SSLContext(PROTOCOL_TLSv1_2)
                ssl_context.set_ciphers("ECDHE+AESGCM:!ECDSA")

                parameters.ssl_options = pika.SSLOptions(context=ssl_context)

            channel = pika.BlockingConnection(parameters).channel()
            if channel.connection.is_open:
                res = HealthCheckStatusEnum.HEALTHY
        except Exception:
            pass

        return res
