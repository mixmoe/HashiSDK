from functools import partial
from json import JSONDecodeError
from typing import Any, Dict, Optional, Union

from httpx import URL, AsyncClient, RequestError

from .log import logger

from .exceptions import APIError

logger = logger.getChild("api")


class IOTClientAPI:
    def __init__(self, qq: int, address: str, timeout: Optional[int] = None) -> None:
        self.qq = qq
        self.address = address + "/v1/LuaApiCaller"
        self.timeout = timeout or 10
        self._post = AsyncClient().post

    async def callAction(
        self, action: str, **kwargs
    ) -> Union[Dict[str, Any], str, int, bytes, None]:

        try:
            response = await self._post(
                URL(
                    self.address,
                    {"qq": self.qq, "timeout": self.timeout, "funcname": action},
                ),
                json=kwargs,
            )
            response.raise_for_status()
        except RequestError as e:
            raise APIError("APIError: " + str(e))

        logger.debug(f"Action {action!r} executed successful with data: {kwargs}.")

        try:
            return response.json()
        except JSONDecodeError:
            pass
        try:
            return response.text
        except UnicodeError:
            pass
        return response.content

    def __getattr__(self, key: str):
        key = key.replace("__", ".")
        return partial(self.callAction, key)

    def __repr__(self) -> str:
        return (
            f"<{self.__class__.__qualname__} object "
            f"(Address:{self.address} Account:{self.qq})>"
        )
