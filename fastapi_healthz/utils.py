import asyncio
import concurrent.futures
from typing import Callable, Any


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
