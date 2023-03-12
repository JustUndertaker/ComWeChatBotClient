"""
将后端与前端ws混入
"""
from functools import wraps
from typing import Union

from fastapi import status
from starlette.websockets import WebSocket, WebSocketDisconnect, WebSocketState
from websockets.exceptions import ConnectionClosed
from websockets.legacy.client import WebSocketClientProtocol

from wechatbot_client.exception import WebSocketClosed
from wechatbot_client.typing import overrides

from .model import Request as BaseRequest
from .model import WebSocket as BaseWebSocket


def fastapi_catch_closed(func):
    """fastapi 的ws 关闭"""

    @wraps(func)
    async def decorator(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except WebSocketDisconnect as e:
            raise WebSocketClosed(e.code)
        except KeyError:
            raise TypeError("WebSocket received unexpected frame type")

    return decorator


def websockets_catch_closed(func):
    """websockets 的 ws 关闭"""

    @wraps(func)
    async def decorator(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except ConnectionClosed as e:
            if e.rcvd_then_sent:
                raise WebSocketClosed(e.rcvd.code, e.rcvd.reason)  # type: ignore
            else:
                raise WebSocketClosed(e.sent.code, e.sent.reason)  # type: ignore

    return decorator


class FastAPIWebSocket(BaseWebSocket):
    """FastAPI WebSocket Wrapper"""

    @overrides(BaseWebSocket)
    def __init__(self, *, request: BaseRequest, websocket: WebSocket) -> None:
        super().__init__(request=request)
        self.websocket = websocket

    @property
    @overrides(BaseWebSocket)
    def closed(self) -> bool:
        return (
            self.websocket.client_state == WebSocketState.DISCONNECTED
            or self.websocket.application_state == WebSocketState.DISCONNECTED
        )

    @overrides(BaseWebSocket)
    async def accept(self) -> None:
        await self.websocket.accept()

    @overrides(BaseWebSocket)
    async def close(
        self, code: int = status.WS_1000_NORMAL_CLOSURE, reason: str = ""
    ) -> None:
        await self.websocket.close(code, reason)

    @overrides(BaseWebSocket)
    async def receive(self) -> Union[str, bytes]:
        # assert self.websocket.application_state == WebSocketState.CONNECTED
        msg = await self.websocket.receive()
        if msg["type"] == "websocket.disconnect":
            raise WebSocketClosed(msg["code"])
        return msg["text"] if "text" in msg else msg["bytes"]

    @overrides(BaseWebSocket)
    @fastapi_catch_closed
    async def receive_text(self) -> str:
        return await self.websocket.receive_text()

    @overrides(BaseWebSocket)
    @fastapi_catch_closed
    async def receive_bytes(self) -> bytes:
        return await self.websocket.receive_bytes()

    @overrides(BaseWebSocket)
    async def send_text(self, data: str) -> None:
        await self.websocket.send({"type": "websocket.send", "text": data})

    @overrides(BaseWebSocket)
    async def send_bytes(self, data: bytes) -> None:
        await self.websocket.send({"type": "websocket.send", "bytes": data})


class BackwardWebSocket(BaseWebSocket):
    """Websockets WebSocket Wrapper"""

    @overrides(BaseWebSocket)
    def __init__(self, *, request: BaseRequest, websocket: WebSocketClientProtocol):
        super().__init__(request=request)
        self.websocket = websocket

    @property
    @overrides(BaseWebSocket)
    def closed(self) -> bool:
        return self.websocket.closed

    @overrides(BaseWebSocket)
    async def accept(self):
        raise NotImplementedError

    @overrides(BaseWebSocket)
    async def close(self, code: int = 1000, reason: str = ""):
        await self.websocket.close(code, reason)

    @overrides(BaseWebSocket)
    @websockets_catch_closed
    async def receive(self) -> Union[str, bytes]:
        return await self.websocket.recv()

    @overrides(BaseWebSocket)
    @websockets_catch_closed
    async def receive_text(self) -> str:
        msg = await self.websocket.recv()
        if isinstance(msg, bytes):
            raise TypeError("WebSocket received unexpected frame type: bytes")
        return msg

    @overrides(BaseWebSocket)
    @websockets_catch_closed
    async def receive_bytes(self) -> bytes:
        msg = await self.websocket.recv()
        if isinstance(msg, str):
            raise TypeError("WebSocket received unexpected frame type: str")
        return msg

    @overrides(BaseWebSocket)
    async def send_text(self, data: str) -> None:
        await self.websocket.send(data)

    @overrides(BaseWebSocket)
    async def send_bytes(self, data: bytes) -> None:
        await self.websocket.send(data)
