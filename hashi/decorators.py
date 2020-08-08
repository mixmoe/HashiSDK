import time
from asyncio import get_running_loop, iscoroutinefunction, run_coroutine_threadsafe
from concurrent.futures.thread import ThreadPoolExecutor
from functools import wraps
from typing import Any, Awaitable, Callable

from .log import logger

EXECUTOR = ThreadPoolExecutor()

logger = logger.getChild("utils")


def _getFuncName(func: Callable):
    return (
        func.__qualname__
        if hasattr(func, "__qualname__")
        else func.__name__
        if hasattr(func, "__name__")
        else repr(func)
    )


def Timing(func: Callable) -> Callable:
    @wraps(func)
    def syncWrapper(*args, **kwargs):
        try:
            beginTime = time.time() * 1000
            return func(*args, **kwargs)
        finally:
            endTime = time.time() * 1000
            logger.trace(
                f"Function {_getFuncName(func)} running cost "
                f"{(endTime-beginTime):.3f}ms."
            )

    @wraps(func)
    async def asyncWrapper(*args, **kwargs):
        try:
            beginTime = time.time() * 1000
            return await func(*args, **kwargs)
        finally:
            endTime = time.time() * 1000
            logger.trace(
                f"Function {_getFuncName(func)} asynchronous running cost "
                f"{(endTime-beginTime):.3f}ms."
            )

    return asyncWrapper if iscoroutinefunction(func) else syncWrapper


def Sync2Async(func: Callable) -> Callable[..., Awaitable[Any]]:
    @wraps(func)
    async def wrapper(*args, **kwargs):
        loop = get_running_loop()
        runner = lambda: Timing(func)(*args, **kwargs)  # noqa: E731
        return await loop.run_in_executor(EXECUTOR, runner)

    return wrapper


def Async2Sync(func: Callable[..., Awaitable[Any]]) -> Callable:
    @wraps(func)
    def wrapper(*args, **kwargs):
        loop = get_running_loop()
        coro = Timing(func)(*args, **kwargs)
        future = run_coroutine_threadsafe(coro, loop)
        return future.result()

    return wrapper
