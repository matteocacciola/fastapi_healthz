from ssl import SSLContext, PROTOCOL_TLSv1_2
try:
    import pika
except ImportError:
    pika = None

from .abstract import HealthCheckAbstract
from ..models import HealthCheckStatusEnum


class HealthCheckRabbitMQ(HealthCheckAbstract):
    def __init__(
        self,
        host: str,
        vhost: str | None = "/",
        username: str | None = None,
        password: str | None = None,
        ssl: bool = True,
        port: int | None = 5672,
    ):
        self.__host = host
        self.__port = port
        self.__vhost = vhost
        self.__username = username
        self.__password = password
        self.__ssl = ssl

    @property
    def service(self) -> str:
        return "rabbitmq"

    @property
    def connection_uri(self) -> str | None:
        secure = "s" if self.__ssl else ""
        return f"amqp{secure}://{self.__host}:{str(self.__port)}"

    @property
    def tags(self) -> list[str]:
        return ["rabbitmq"]

    @property
    def comments(self) -> list[str]:
        return []

    def check_health(self) -> HealthCheckStatusEnum:
        if pika is None:
            raise ImportError("pika is not installed. Install it with `pip install fastapi-healthz[rabbitmq]`.")

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
