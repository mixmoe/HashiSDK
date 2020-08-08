import asyncio
from functools import partial, wraps
from inspect import iscoroutinefunction
from itertools import count
from typing import Any, Awaitable, Callable, Dict, List, NoReturn, Optional, Union

from pydantic import ValidationError
from socketio import AsyncClient as SocketIOClient
from socketio.exceptions import SocketIOError

from .decorators import Sync2Async, Timing
from .log import logger

from .api import IOTClientAPI
from .exceptions import NetworkError
from .models import EventMessage, FriendMessage, GroupMessage

EventHandler_T = Callable[[Dict[str, Any]], Awaitable[None]]
EventListener_T = Callable[[EventMessage], Awaitable[None]]
FriendMessageListener_T = Callable[[FriendMessage], Awaitable[None]]
GroupMessageListener_T = Callable[[GroupMessage], Awaitable[None]]


def _exceptionProcessor(exceptions: List[Exception]):
    for exception in exceptions:
        try:
            raise exception
        except Exception as e:
            logger.exception(f"Exception {e!r} occurred:")
    return


class IOTClient:
    def __init__(
        self,
        host: str,
        port: int,
        qq: int,
        /,
        heartbeat: Optional[int] = None,
        timeout: Optional[int] = None,
    ):
        self.host = host
        self.port = port
        self.qq = qq
        self.api = IOTClientAPI(qq=qq, address=self.address, timeout=timeout or 10)

        self._heartbeatInterval = heartbeat
        self._heartbeatTask: Optional[asyncio.Task] = None
        self._socketIO: Optional[SocketIOClient] = None

        self._eventListener: List[EventListener_T] = []
        self._friendMessageListener: List[FriendMessageListener_T] = []
        self._groupMessageListener: List[GroupMessageListener_T] = []

        self._log = lambda *msg: logger.getChild("message").info(" - ".join(msg))

    @property
    def address(self) -> str:
        return f"http://{self.host}:{self.port}"

    @property
    def socket(self) -> SocketIOClient:
        if self._socketIO is None:
            self._socketIO = SocketIOClient()
        return self._socketIO

    @property
    def listeners(
        self,
    ) -> Dict[
        str,
        Union[
            List[EventListener_T],
            List[FriendMessageListener_T],
            List[GroupMessageListener_T],
        ],
    ]:
        return {
            "event": self._eventListener.copy(),
            "friend": self._friendMessageListener.copy(),
            "group": self._groupMessageListener.copy(),
        }

    def _on(self, event: str, handler: Optional[EventHandler_T] = None, /):
        if handler is None:
            return partial(self._on, event)

        @Timing
        @wraps(handler)
        @self.socket.on(event)
        async def wrapper(data: Dict[str, Any]):
            data.update(data.pop("CurrentPacket"))
            try:
                return await handler(data)  # type: ignore
            except ValidationError:
                logger.exception("Serialization of message failed:")

        return wrapper

    async def _eventHandler(self, data: Dict[str, Any]):
        serializedData = EventMessage(**data)
        self._log(
            f"Current: {serializedData.CurrentQQ}",
            f"Event: {serializedData.Data.EventName}",
            f"{serializedData.Data.EventMsg!r}",
        )
        result: List[Optional[Exception]] = await asyncio.gather(
            *map(lambda func: func(serializedData.copy()), self._eventListener),
            return_exceptions=True,
        )

        failed = [*filter(lambda o: isinstance(o, Exception), result)]
        _exceptionProcessor(failed)  # type:ignore
        logger.debug(
            f"Event handler handled data: {data!r}, "
            f"total {len(result)} listeners, {len(failed)} failed."
        )

    async def _friendMessageHandler(self, data: Dict[str, Any]):
        serializedData = FriendMessage(**data)
        if serializedData.CurrentQQ == serializedData.Data.FromUin:
            return
        self._log(
            f"Current: {serializedData.CurrentQQ}",
            f"From: {serializedData.Data.FromUin}",
            f"{serializedData.Data.Content!r}",
        )
        result: List[Optional[Exception]] = await asyncio.gather(
            *map(
                lambda func: func(serializedData.copy()), self._friendMessageListener,
            ),
            return_exceptions=True,
        )

        failed = [*filter(lambda o: isinstance(o, Exception), result)]
        _exceptionProcessor(failed)  # type:ignore
        logger.debug(
            f"Message handler handled data: {data!r}, "
            f"total {len(result)} listeners, {len(failed)} failed."
        )

    async def _groupMessageHandler(self, data: Dict[str, Any]):
        serializedData = GroupMessage(**data)
        if serializedData.CurrentQQ == serializedData.Data.FromUserId:
            return
        self._log(
            f"Current: {serializedData.CurrentQQ}",
            f"Group: {serializedData.Data.FromGroupId}",
            f"From: {serializedData.Data.FromUserId}",
            f"{serializedData.Data.Content!r}",
        )
        result: List[Optional[Exception]] = await asyncio.gather(
            *map(lambda func: func(serializedData.copy()), self._groupMessageListener),
            return_exceptions=True,
        )

        failed = [*filter(lambda o: isinstance(o, Exception), result)]
        _exceptionProcessor(failed)  # type:ignore
        logger.debug(
            f"Message handler handled data: {data!r}, "
            f"total {len(result)} listeners, {len(failed)} failed."
        )

    def init(self):
        async def heartbeatTask() -> NoReturn:  # type:ignore
            interval = self._heartbeatInterval
            assert interval is not None and interval > 0
            logger.info(
                f"Heartbeat scheduler started, the interval is {interval} seconds."
            )
            for i in count():
                await asyncio.sleep(1)
                if not self.socket.connected:
                    break
                if i % interval != 0:
                    continue
                await self.heartbeat()
                logger.info("Heartbeat event is pushed to server successfully.")

        if self._heartbeatInterval is not None:
            self.socket.on("connect", heartbeatTask)

        self._on("OnEvents", self._eventHandler)
        self._on("OnFriendMsgs", self._friendMessageHandler)
        self._on("OnGroupMsgs", self._groupMessageHandler)

        logger.info(f"Provider {self} initialized.")

    async def heartbeat(self):
        await self.socket.emit(
            "GetWebConn",
            data=str(self.qq),
            callback=lambda x: logger.debug("Callback of heartbeat received: %r" % x),
        )

    async def connect(self) -> None:
        try:
            await self.socket.connect(self.address, transports=["websocket"])
        except SocketIOError:
            raise NetworkError
        logger.info(f"Connection to {self.address!r} is established.")

    async def run(self) -> NoReturn:  # type:ignore
        await self.connect()
        try:
            await self.socket.wait()
        finally:
            await self.socket.disconnect()

    def onEvent(self, func: EventListener_T) -> EventListener_T:
        func = func if iscoroutinefunction(func) else Sync2Async(func)  # type:ignore
        self._eventListener.append(func)
        return func

    def onFirendMessage(self, func: FriendMessageListener_T) -> FriendMessageListener_T:
        func = func if iscoroutinefunction(func) else Sync2Async(func)  # type:ignore
        self._friendMessageListener.append(func)
        return func

    def onGroupMessage(self, func: GroupMessageListener_T) -> GroupMessageListener_T:
        func = func if iscoroutinefunction(func) else Sync2Async(func)  # type:ignore
        self._groupMessageListener.append(func)
        return func

    def __repr__(self):
        return (
            f"<{self.__class__.__qualname__} object "
            f"(Address:{self.address} Account:{self.qq})>"
        )

