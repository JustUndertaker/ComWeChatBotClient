"""
adapter,用来管理driver和websocket
"""
import asyncio
import contextlib
import json
from abc import abstractmethod
from typing import Any, AsyncGenerator, Generator, Optional, Type, cast

import msgpack
from pydantic import ValidationError

from wechatbot_client.action_manager import (
    ActionRequest,
    ActionResponse,
    WsActionRequest,
    WsActionResponse,
)
from wechatbot_client.config import Config
from wechatbot_client.consts import IMPL, ONEBOT_VERSION, USER_AGENT
from wechatbot_client.driver import (
    URL,
    Driver,
    ForwardWebSocket,
    HTTPServerSetup,
    Request,
    Response,
    WebSocket,
    WebSocketServerSetup,
)
from wechatbot_client.exception import WebSocketClosed
from wechatbot_client.onebot12 import Event
from wechatbot_client.utils import escape_tag, logger_wrapper

from .utils import flattened_to_nested, get_auth_bearer

log = logger_wrapper("OneBot V12")


class Adapter:
    """
    适配器，用来处理websocket连接
    """

    config: Config
    """应用设置"""
    event_models: dict
    """事件模型映射"""
    tasks: list[asyncio.Task]
    """反向连接ws任务列表"""
    driver: Driver
    """后端驱动"""

    def __init__(self, config: Config) -> None:
        self.config = config
        self.driver = Driver(config)
        self.tasks = []

    def setup_http_server(self, setup: HTTPServerSetup) -> None:
        """设置一个 HTTP 服务器路由配置"""
        self.driver.setup_http_server(setup)

    def setup_websocket_server(self, setup: WebSocketServerSetup) -> None:
        """设置一个 WebSocket 服务器路由配置"""
        self.driver.setup_websocket_server(setup)

    async def request(self, setup: Request) -> Response:
        """进行一个 HTTP 客户端请求"""
        return await self.driver.request(setup)

    @contextlib.asynccontextmanager
    async def websocket(self, setup: Request) -> AsyncGenerator[ForwardWebSocket, None]:
        """建立一个 WebSocket 客户端连接请求"""
        async with self.driver.websocket(setup) as ws:
            yield ws

    def _check_access_token(self, request: Request) -> Optional[Response]:
        """
        检测access_token
        """
        token = get_auth_bearer(request.headers.get("Authorization"))

        access_token = self.config.access_token
        if access_token != "" and access_token != token:
            msg = (
                "Authorization Header is invalid"
                if token
                else "Missing Authorization Header"
            )
            log("WARNING", msg)
            return Response(403, content=msg)

    async def handle_ws(self, websocket: WebSocket) -> None:
        """
        当有新的ws连接时的任务
        """

        # check access_token
        response = self._check_access_token(websocket.request)
        if response is not None:
            content = cast(str, response.content)
            await websocket.close(1008, content)
            return

        # 后续处理代码
        seq = self.driver.ws_connect(websocket)
        log("SUCCESS", f"新的websocket连接，编号为: {seq}...")

        try:
            while True:
                data = await websocket.receive()
                raw_data = (
                    json.loads(data) if isinstance(data, str) else msgpack.unpackb(data)
                )
                if action := self.json_to_ws_action(raw_data):
                    response = await self.action_ws_request(action)
                    await websocket.send(response.json(ensure_ascii=False))
        except WebSocketClosed:
            log(
                "WARNING",
                f"编号为: {seq} 的websocket被远程关闭了...",
            )
        except Exception as e:
            log(
                "ERROR",
                "<r><bg #f8bbd0>处理来自 websocket 的数据时出错 "
                f"- 编号: {seq}.</bg #f8bbd0></r>",
                e,
            )

        finally:
            with contextlib.suppress(Exception):
                await websocket.close()
            self.driver.ws_disconnect(seq)

    async def handle_http(self, request: Request) -> Response:
        """处理http任务"""
        self_id = request.headers.get("x-self-id")

        # check self_id
        if not self_id:
            log("WARNING", "Missing X-Self-ID Header")
            return Response(400, content="Missing X-Self-ID Header")

        # check access_token
        response = self._check_access_token(request)
        if response is not None:
            return response

        data = request.content
        if data is not None:
            json_data = json.loads(data)
            if action := self.json_to_action(json_data):
                response = await self.action_request(action)
                headers = {
                    "Content-Type": "application/json",
                    "User-Agent": USER_AGENT,
                    "X-Impl": IMPL,
                    "X-OneBot-Version": f"{ONEBOT_VERSION}",
                }
                if self.config.access_token != "":
                    headers["Authorization"] = f"Bearer {self.config.access_token}"
                return Response(
                    200, headers=headers, content=response.json(ensure_ascii=False)
                )
        return Response(204)

    async def start_backward(self) -> None:
        """
        开启反向ws连接应用端
        """
        try:
            ws_url = URL(self.config.websocket_url)
            self.tasks.append(asyncio.create_task(self._backward_ws(ws_url)))
        except Exception as e:
            log(
                "ERROR",
                f"<r><bg #f8bbd0>Bad url {escape_tag(self.config.websocket_url)} "
                "in websocket_url config</bg #f8bbd0></r>",
                e,
            )

    async def _backward_ws(self, url: URL) -> None:
        """
        反向ws连接任务
        """
        headers = {
            "User-Agent": USER_AGENT,
            "Sec-WebSocket-Protocol": f"{ONEBOT_VERSION}.{IMPL}",
        }
        if self.config.access_token != "":
            headers["Authorization"] = f"Bearer {self.config.access_token}"
        req = Request("GET", url, headers=headers, timeout=30.0)
        log("DEBUG", f"<y>正在连接到url: {url}</y>")
        while True:
            try:
                async with self.websocket(req) as ws:
                    log(
                        "DEBUG",
                        f"WebSocket Connection to {escape_tag(str(url))} established",
                    )
                    seq = self.driver.ws_connect(ws)
                    log("SUCCESS", f"<y>新的websocket连接，编号为: {seq}...")
                    try:
                        while True:
                            data = await ws.receive()
                            raw_data = (
                                json.loads(data)
                                if isinstance(data, str)
                                else msgpack.unpackb(data)
                            )
                            if action := self.json_to_ws_action(raw_data):
                                response = await self.action_ws_request(action)
                                await ws.send(response.json(ensure_ascii=False))
                    except WebSocketClosed as e:
                        log(
                            "ERROR",
                            "<r><bg #f8bbd0>WebSocket 关闭了...</bg #f8bbd0></r>",
                            e,
                        )
                    except Exception as e:
                        log(
                            "ERROR",
                            "<r><bg #f8bbd0>处理来自 websocket 的数据时出错"
                            f"{escape_tag(str(url))} 正在尝试重连...</bg #f8bbd0></r>",
                            e,
                        )
                    finally:
                        self.driver.ws_disconnect(seq)

            except Exception as e:
                log(
                    "ERROR",
                    "<r><bg #f8bbd0>连接到 "
                    f"{escape_tag(str(url))} 时出错{e} 正在尝试重连...</bg #f8bbd0></r>",
                )

            await asyncio.sleep(self.config.reconnect_interval / 1000)

    async def stop_backward(self) -> None:
        """关闭反向ws连接任务"""
        for task in self.tasks:
            if not task.done():
                task.cancel()

    @classmethod
    def get_event_model(
        cls, data: dict[str, Any]
    ) -> Generator[Type[Event], None, None]:
        """根据事件获取对应 `Event Model` 及 `FallBack Event Model` 列表。"""
        key = f"/{data.get('impl')}/{data.get('platform')}"
        if key in cls.event_models:
            yield from cls.event_models[key].get_model(data)
        yield from cls.event_models[""].get_model(data)

    @classmethod
    def json_to_event(cls, json_data: Any) -> Optional[Event]:
        """
        反序列化event
        """
        if not isinstance(json_data, dict):
            return None

        # transform flattened dict to nested
        json_data = flattened_to_nested(json_data)

        try:
            for model in cls.get_event_model(json_data):
                try:
                    event = model.parse_obj(json_data)
                    break
                except Exception as e:
                    log("DEBUG", "Event Parse Error", e)
            else:
                event = Event.parse_obj(json_data)
            return event

        except Exception as e:
            log(
                "ERROR",
                "<r><bg #f8bbd0>Failed to parse event. "
                f"Raw: {str(json_data)}</bg #f8bbd0></r>",
                e,
            )
            return None

    @classmethod
    def json_to_action(cls, json_data: Any) -> Optional[ActionRequest]:
        """
        json转换为action
        """
        if not isinstance(json_data, dict):
            return None
        try:
            action = ActionRequest.parse_obj(json_data)
        except ValidationError:
            return None
        return action

    @classmethod
    def json_to_ws_action(cls, json_data: Any) -> Optional[WsActionRequest]:
        """json转换为wsaction"""
        if not isinstance(json_data, dict):
            return None
        try:
            echo = json_data.pop("echo")
        except Exception:
            return None
        action = cls.json_to_action(json_data)
        if action is None:
            return None
        return WsActionRequest(echo=echo, **action.dict())

    @abstractmethod
    async def action_request(self, request: ActionRequest) -> ActionResponse:
        """
        处理action的方法
        """
        raise NotImplementedError

    @abstractmethod
    async def action_ws_request(self, request: WsActionRequest) -> WsActionResponse:
        """
        处理wsaction的方法
        """
        raise NotImplementedError
