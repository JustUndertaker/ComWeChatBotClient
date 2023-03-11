"""

"""


import contextlib
import logging
from functools import wraps
from typing import Any, Callable, Dict, List, Optional, Tuple, Union

import httpx
import uvicorn
from fastapi import FastAPI, Request, UploadFile, status
from fastapi.responses import Response
from pydantic import BaseSettings
from starlette.websockets import WebSocket, WebSocketDisconnect, WebSocketState

from wechatbot_client.config import Config as BaseConfig
from wechatbot_client.exception import WebSocketClosed
from wechatbot_client.typing import overrides

from .model import FileTypes, HTTPServerSetup, HTTPVersion
from .model import Request as BaseRequest
from .model import Response as BaseResponse
from .model import WebSocket as BaseWebSocket
from .model import WebSocketServerSetup


def catch_closed(func):
    @wraps(func)
    async def decorator(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except WebSocketDisconnect as e:
            raise WebSocketClosed(e.code)
        except KeyError:
            raise TypeError("WebSocket received unexpected frame type")

    return decorator


class Config(BaseSettings):
    """FastAPI 驱动框架设置，详情参考 FastAPI 文档"""

    fastapi_openapi_url: Optional[str] = None
    """`openapi.json` 地址，默认为 `None` 即关闭"""
    fastapi_docs_url: Optional[str] = None
    """`swagger` 地址，默认为 `None` 即关闭"""
    fastapi_redoc_url: Optional[str] = None
    """`redoc` 地址，默认为 `None` 即关闭"""
    fastapi_include_adapter_schema: bool = True
    """是否包含适配器路由的 schema，默认为 `True`"""
    fastapi_reload: bool = False
    """开启/关闭冷重载"""
    fastapi_reload_dirs: Optional[List[str]] = None
    """重载监控文件夹列表，默认为 uvicorn 默认值"""
    fastapi_reload_delay: float = 0.25
    """重载延迟，默认为 uvicorn 默认值"""
    fastapi_reload_includes: Optional[List[str]] = None
    """要监听的文件列表，支持 glob pattern，默认为 uvicorn 默认值"""
    fastapi_reload_excludes: Optional[List[str]] = None
    """不要监听的文件列表，支持 glob pattern，默认为 uvicorn 默认值"""
    fastapi_extra: Dict[str, Any] = {}
    """传递给 `FastAPI` 的其他参数。"""

    class Config:
        extra = "ignore"


class Driver:
    """FastAPI 驱动框架。"""

    def __init__(self, config: BaseConfig) -> None:
        self.config = config
        self.fastapi_config: Config = Config(**config.dict())

        self._server_app = FastAPI(
            openapi_url=self.fastapi_config.fastapi_openapi_url,
            docs_url=self.fastapi_config.fastapi_docs_url,
            redoc_url=self.fastapi_config.fastapi_redoc_url,
            **self.fastapi_config.fastapi_extra,
        )

    def type(self) -> str:
        """驱动名称: `fastapi`"""
        return "fastapi"

    def server_app(self) -> FastAPI:
        """`FastAPI APP` 对象"""
        return self._server_app

    @property
    def asgi(self) -> FastAPI:
        """`FastAPI APP` 对象"""
        return self._server_app

    @property
    def logger(self) -> logging.Logger:
        """fastapi 使用的 logger"""
        return logging.getLogger("fastapi")

    def setup_http_server(self, setup: HTTPServerSetup) -> None:
        """设置一个 HTTP 服务器路由配置"""

        async def _handle(request: Request) -> Response:
            return await self._handle_http(request, setup)

        self._server_app.add_api_route(
            setup.path.path,
            _handle,
            name=setup.name,
            methods=[setup.method],
            include_in_schema=self.fastapi_config.fastapi_include_adapter_schema,
        )

    def setup_websocket_server(self, setup: WebSocketServerSetup) -> None:
        """设置一个 WebSocket 服务器路由配置"""

        async def _handle(websocket: WebSocket) -> None:
            await self._handle_ws(websocket, setup)

        self._server_app.add_api_websocket_route(
            setup.path.path,
            _handle,
            name=setup.name,
        )

    def on_startup(self, func: Callable) -> Callable:
        """注册一个在驱动器启动时执行的函数，参考文档: [Events](https://fastapi.tiangolo.com/advanced/events/#startup-event)"""
        return self.server_app.on_event("startup")(func)

    def on_shutdown(self, func: Callable) -> Callable:
        """注册一个在驱动器停止时执行的函数，参考文档: [Events](https://fastapi.tiangolo.com/advanced/events/#shutdown-event)"""
        return self.server_app.on_event("shutdown")(func)

    def run(
        self,
        host: Optional[str] = None,
        port: Optional[int] = None,
        *,
        app: Optional[str] = None,
        **kwargs,
    ) -> None:
        """使用 `uvicorn` 启动 FastAPI"""
        LOGGING_CONFIG = {
            "version": 1,
            "disable_existing_loggers": False,
            "handlers": {
                "default": {
                    "class": "nonebot.log.LoguruHandler",
                },
            },
            "loggers": {
                "uvicorn.error": {"handlers": ["default"], "level": "INFO"},
                "uvicorn.access": {
                    "handlers": ["default"],
                    "level": "INFO",
                },
            },
        }
        uvicorn.run(
            app or self.server_app,  # type: ignore
            host=host or str(self.config.host),
            port=port or self.config.port,
            reload=self.fastapi_config.fastapi_reload,
            reload_dirs=self.fastapi_config.fastapi_reload_dirs,
            reload_delay=self.fastapi_config.fastapi_reload_delay,
            reload_includes=self.fastapi_config.fastapi_reload_includes,
            reload_excludes=self.fastapi_config.fastapi_reload_excludes,
            log_config=LOGGING_CONFIG,
            **kwargs,
        )

    async def _handle_http(
        self,
        request: Request,
        setup: HTTPServerSetup,
    ) -> Response:
        json: Any = None
        with contextlib.suppress(Exception):
            json = await request.json()

        data: Optional[dict] = None
        files: Optional[List[Tuple[str, FileTypes]]] = None
        with contextlib.suppress(Exception):
            form = await request.form()
            data = {}
            files = []
            for key, value in form.multi_items():
                if isinstance(value, UploadFile):
                    files.append(
                        (key, (value.filename, value.file, value.content_type))
                    )
                else:
                    data[key] = value

        http_request = BaseRequest(
            request.method,
            str(request.url),
            headers=request.headers.items(),
            cookies=request.cookies,
            content=await request.body(),
            data=data,
            json=json,
            files=files,
            version=request.scope["http_version"],
        )

        response = await setup.handle_func(http_request)
        return Response(
            response.content, response.status_code, dict(response.headers.items())
        )

    async def _handle_ws(
        self, websocket: WebSocket, setup: WebSocketServerSetup
    ) -> None:
        request = BaseRequest(
            "GET",
            str(websocket.url),
            headers=websocket.headers.items(),
            cookies=websocket.cookies,
            version=websocket.scope.get("http_version", "1.1"),
        )
        ws = FastAPIWebSocket(
            request=request,
            websocket=websocket,
        )

        await setup.handle_func(ws)

    async def request(self, setup: BaseRequest) -> BaseResponse:
        """
        发起一个http请求
        """
        async with httpx.AsyncClient(
            cookies=setup.cookies.jar,
            http2=setup.version == HTTPVersion.H2,
            proxies=setup.proxy,
            follow_redirects=True,
        ) as client:
            response = await client.request(
                setup.method,
                str(setup.url),
                content=setup.content,
                data=setup.data,
                json=setup.json,
                files=setup.files,
                headers=tuple(setup.headers.items()),
                timeout=setup.timeout,
            )
            return Response(
                response.status_code,
                headers=response.headers.multi_items(),
                content=response.content,
                request=setup,
            )


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
    @catch_closed
    async def receive_text(self) -> str:
        return await self.websocket.receive_text()

    @overrides(BaseWebSocket)
    @catch_closed
    async def receive_bytes(self) -> bytes:
        return await self.websocket.receive_bytes()

    @overrides(BaseWebSocket)
    async def send_text(self, data: str) -> None:
        await self.websocket.send({"type": "websocket.send", "text": data})

    @overrides(BaseWebSocket)
    async def send_bytes(self, data: bytes) -> None:
        await self.websocket.send({"type": "websocket.send", "bytes": data})
