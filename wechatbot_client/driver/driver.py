"""
后端驱动driver
"""
import contextlib
import logging
import sys
from typing import Any, AsyncGenerator, Callable, Optional, Tuple, Union

import httpx
import uvicorn
from fastapi import FastAPI, Request, UploadFile
from fastapi.responses import Response
from pydantic import BaseSettings
from starlette.websockets import WebSocket
from websockets.legacy.client import Connect

from wechatbot_client.config import Config as BaseConfig
from wechatbot_client.consts import IMPL, ONEBOT_VERSION

from .base import BackwardWebSocket, FastAPIWebSocket
from .model import FileTypes, HTTPServerSetup, HTTPVersion
from .model import Request as BaseRequest
from .model import Response as BaseResponse
from .model import WebSocketServerSetup


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
    fastapi_reload_dirs: Optional[list[str]] = None
    """重载监控文件夹列表，默认为 uvicorn 默认值"""
    fastapi_reload_delay: float = 0.25
    """重载延迟，默认为 uvicorn 默认值"""
    fastapi_reload_includes: Optional[list[str]] = None
    """要监听的文件列表，支持 glob pattern，默认为 uvicorn 默认值"""
    fastapi_reload_excludes: Optional[list[str]] = None
    """不要监听的文件列表，支持 glob pattern，默认为 uvicorn 默认值"""
    fastapi_extra: dict[str, Any] = {}
    """传递给 `FastAPI` 的其他参数。"""

    class Config:
        extra = "ignore"


class Driver:
    """FastAPI 驱动框架。"""

    connects: dict[int, Union[FastAPIWebSocket, BackwardWebSocket]]
    """维护的连接字典"""
    _seq: int

    def __init__(self, config: BaseConfig) -> None:
        self._seq = 0
        self.connects = {}
        self.config = config
        self.fastapi_config: Config = Config(**config.dict())

        self._server_app = FastAPI(
            openapi_url=self.fastapi_config.fastapi_openapi_url,
            docs_url=self.fastapi_config.fastapi_docs_url,
            redoc_url=self.fastapi_config.fastapi_redoc_url,
            **self.fastapi_config.fastapi_extra,
        )

    def get_seq(self) -> int:
        """获取一个seq，用来维护ws连接"""
        s = self._seq
        self._seq = (self._seq + 1) % sys.maxsize
        return s

    def type(self) -> str:
        """驱动名称: `fastapi`"""
        return "fastapi"

    @property
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
                    "class": "wechatbot_client.log.LoguruHandler",
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
        files: Optional[list[Tuple[str, FileTypes]]] = None
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

    @contextlib.asynccontextmanager
    async def start_websocket(
        self, setup: BaseRequest
    ) -> AsyncGenerator["BackwardWebSocket", None]:
        """创建一个websocket连接请求"""
        connection = Connect(
            str(setup.url),
            subprotocols=[f"{ONEBOT_VERSION}.{IMPL}"],
            extra_headers={**setup.headers, **setup.cookies.as_header(setup)},
            open_timeout=setup.timeout,
            max_size=(2**20) * self.config.websocket_buffer_size,
        )
        async with connection as ws:
            yield BackwardWebSocket(request=setup, websocket=ws)

    def ws_connect(self, websocket: Union[FastAPIWebSocket, BackwardWebSocket]) -> int:
        """
        添加websoket连接,返回一个seq
        """
        seq = self.get_seq()
        self.connects[seq] = websocket
        return seq

    def ws_disconnect(self, seq: int) -> None:
        """ws断开连接"""
        self.connects.pop(seq)

    def check_websocket_in(
        self, websocket: Union[FastAPIWebSocket, BackwardWebSocket]
    ) -> bool:
        """
        检测websocket是否在维护字典中
        """
        return websocket in self.connects.keys()
