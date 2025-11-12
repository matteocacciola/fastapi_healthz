import asyncio
import concurrent.futures
from enum import Enum as BaseEnum, EnumMeta
from typing import Callable, Any


class MetaEnum(EnumMeta):
    """
    Enables the use of the `in` operator for enums.
    For example:
    if el not in Elements:
        raise ValueError("invalid element")
    """
    def __contains__(cls, item):
        try:
            cls(item)
        except ValueError:
            return False
        return True


class Enum(BaseEnum, metaclass=MetaEnum):
    def __str__(self):
        return self.value

    def __eq__(self, other):
        if isinstance(other, Enum):
            return self.value == other.value
        return self.value == other

    def __hash__(self):
        return hash(self.value)


def run_sync_async(callback: Callable[..., Any], *args, **kwargs) -> Any:
    if not asyncio.iscoroutinefunction(callback) and not asyncio.iscoroutine(callback):
        return callback(*args, **kwargs)

    coro = callback(*args, **kwargs)

    try:
        asyncio.get_running_loop()

        def run_async_in_thread():
            return asyncio.run(coro)

        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(run_async_in_thread)
            return future.result()
    except RuntimeError:
        return asyncio.run(coro)
