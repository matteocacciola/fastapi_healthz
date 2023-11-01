from typing import Callable, Any
from starlette.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from .registry import HealthCheckRegistry
from .models import HealthCheckStatusEnum


def health_check_route(registry: HealthCheckRegistry) -> Callable:
    """
    This function is passed to the add_api_route with the built factory.

    When called, the endpoint method within, will be called and it will run the job bound to the factory.
    The results will be parsed and sent back to the requestor via JSON.
    """

    def encode_json(value: Any) -> Any:
        """
        Encodes the provided value as a JSON column.
        :param value: the value to encode
        :return: the encoded value
        """
        return jsonable_encoder({} if value is None else value)

    def endpoint() -> JSONResponse:
        res = registry.check()
        if res["status"] == HealthCheckStatusEnum.UNHEALTHY:
            return JSONResponse(content=encode_json(res), status_code=500)
        return JSONResponse(content=encode_json(res), status_code=200)

    return endpoint
