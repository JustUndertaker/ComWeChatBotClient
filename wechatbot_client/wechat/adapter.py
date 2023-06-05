"""
adapter,用来管理driver和websocket
"""
import asyncio
import contextlib
import json
import time
from abc import abstractmethod
from typing import Any, AsyncGenerator, Optional, Union, cast
from uuid import uuid4

import msgpack
from pydantic import ValidationError

from wechatbot_client.action_manager import (
    ActionRequest,
    ActionResponse,
    WsActionRequest,
    WsActionResponse,
)
from wechatbot_client.config import Config, WebsocketType
from wechatbot_client.consts import IMPL, ONEBOT_VERSION, USER_AGENT, VERSION
from wechatbot_client.driver import (
    URL,
    BackwardWebSocket,
    Driver,
    FastAPIWebSocket,
    HTTPServerSetup,
    Request,
    Response,
    WebSocket,
    WebSocketServerSetup,
)
from wechatbot_client.exception import WebSocketClosed
from wechatbot_client.onebot12 import ConnectEvent, Event, StatusUpdateEvent
from wechatbot_client.utils import DataclassEncoder, escape_tag, logger_wrapper

from .utils import get_auth_bearer

log = logger_wrapper("OneBot V12")

HTTP_EVENT_LIST: list[Event] = []
"""get_latest_events的event储存"""


def get_connet_event() -> ConnectEvent:
    """
    生成连接事件
    """
    event_id = str(uuid4())
    data = {
        "impl": IMPL,
        "version": VERSION,
        "onebot_version": ONEBOT_VERSION,
    }
    return ConnectEvent(id=event_id, time=time.time(), version=data)


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
    async def start_websocket(
        self, setup: Request
    ) -> AsyncGenerator[BackwardWebSocket, None]:
        """建立一个 WebSocket 客户端连接请求"""
        async with self.driver.start_websocket(setup) as ws:
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
        await websocket.accept()
        seq = self.driver.ws_connect(websocket)
        log("SUCCESS", f"新的websocket连接，编号为: {seq}...")
        # 发送元事件
        event = get_connet_event()
        try:
            await websocket.send(event.json(ensure_ascii=False))
        except Exception as e:
            log("ERROR", f"发送connect事件失败:{e}")
        # 发送update事件
        event = self.get_status_update_event()
        try:
            await websocket.send(event.json(ensure_ascii=False, cls=DataclassEncoder))
        except Exception as e:
            log("ERROR", f"发送status_update事件失败:{e}")
        try:
            while True:
                data = await websocket.receive()
                raw_data = (
                    json.loads(data) if isinstance(data, str) else msgpack.unpackb(data)
                )
                if action := self.json_to_ws_action(raw_data):
                    response = await self.action_ws_request(action)
                    await websocket.send(
                        response.json(ensure_ascii=False, cls=DataclassEncoder)
                    )
        except WebSocketClosed:
            log(
                "WARNING",
                f"编号为: {seq} 的websocket被远程关闭了...",
            )
        except Exception as e:
            log(
                "ERROR",
                f"<r><bg #f8bbd0>处理来自 websocket 的数据时出错 :{e} "
                f"- 编号: {seq}.</bg #f8bbd0></r>",
            )

        finally:
            with contextlib.suppress(Exception):
                await websocket.close()
            self.driver.ws_disconnect(seq)

    async def handle_http(self, request: Request) -> Response:
        """处理http任务"""

        # check access_token
        response = self._check_access_token(request)
        if response is not None:
            return response

        data = request.content
        if data is not None:
            json_data = json.loads(data)
            if action := self.json_to_action(json_data):
                # get_latest_events处理
                if action.action == "get_latest_events":
                    if not self.config.event_enabled:
                        response = ActionResponse(
                            status="failed",
                            retcode=10002,
                            data=None,
                            message="未开启该action",
                        )
                    else:
                        data = HTTP_EVENT_LIST.copy()
                        HTTP_EVENT_LIST.clear()
                        response = ActionResponse(status="ok", retcode=0, data=data)
                else:
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
                    200,
                    headers=headers,
                    content=response.json(
                        by_alias=True, ensure_ascii=False, cls=DataclassEncoder
                    ),
                )
        return Response(204)

    async def start_backward(self) -> None:
        """
        开启反向ws连接应用端
        """
        for url in self.config.websocket_url:
            try:
                ws_url = URL(url)
                self.tasks.append(asyncio.create_task(self._backward_ws(ws_url)))
            except Exception as e:
                log(
                    "ERROR",
                    f"<r><bg #f8bbd0>Bad url {escape_tag(url)} "
                    "in websocket_url config</bg #f8bbd0></r>",
                    e,
                )

    async def _backward_ws(self, url: URL) -> None:
        """
        反向ws连接任务
        """
        headers = {
            "User-Agent": USER_AGENT,
        }
        if self.config.access_token != "":
            headers["Authorization"] = f"Bearer {self.config.access_token}"
        setup = Request("GET", url, headers=headers, timeout=5.0)
        log("DEBUG", f"<y>正在连接到url: {url}</y>")
        while True:
            try:
                async with self.start_websocket(setup) as websocket:
                    log(
                        "SUCCESS",
                        f"WebSocket Connection to {escape_tag(str(url))} established",
                    )
                    seq = self.driver.ws_connect(websocket)
                    log("SUCCESS", f"<y>新的websocket连接，编号为: {seq}...</y>")
                    # 发送connect事件
                    event = get_connet_event()
                    try:
                        await websocket.send(
                            event.json(ensure_ascii=False, cls=DataclassEncoder)
                        )
                    except Exception as e:
                        log("ERROR", f"发送connect事件失败:{e}")
                    # 发送update事件
                    event = self.get_status_update_event()
                    try:
                        await websocket.send(
                            event.json(ensure_ascii=False, cls=DataclassEncoder)
                        )
                    except Exception as e:
                        log("ERROR", f"发送status_update事件失败:{e}")
                    try:
                        while True:
                            data = await websocket.receive()
                            raw_data = (
                                json.loads(data)
                                if isinstance(data, str)
                                else msgpack.unpackb(data)
                            )
                            if action := self.json_to_ws_action(raw_data):
                                response = await self.action_ws_request(action)
                                await websocket.send(
                                    response.json(
                                        ensure_ascii=False, cls=DataclassEncoder
                                    )
                                )
                    except WebSocketClosed as e:
                        log(
                            "ERROR",
                            f"<r><bg #f8bbd0>WebSocket 关闭了...</bg #f8bbd0></r>: {e}",
                        )
                    except Exception as e:
                        log(
                            "ERROR",
                            f"<r><bg #f8bbd0>处理来自 websocket 的数据时出错: {e}"
                            f"{escape_tag(str(url))} 正在尝试重连...</bg #f8bbd0></r>",
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
    def json_to_action(cls, json_data: Any) -> Optional[ActionRequest]:
        """
        json转换为action
        """
        if not isinstance(json_data, dict):
            return None
        try:
            action = ActionRequest.parse_obj(json_data)
        except ValidationError:
            log("ERROR", f"<r>action请求错误: </r>{json_data}")
            return None
        logstring = str(action.dict())
        if len(logstring) > 200:
            logstring = logstring[:200] + "..."
        log("SUCCESS", f"<y>收到action请求: </y>{logstring}")
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
    def get_status_update_event(slef) -> StatusUpdateEvent:
        """
        获取状态更新事件
        """
        raise NotImplementedError

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

    async def http_event(self, event: Event) -> None:
        """
        http处理event
        """
        global HTTP_EVENT_LIST
        if self.config.event_enabled:
            # 开启 get_latest_events
            if (
                self.config.event_buffer_size != 0
                and len(HTTP_EVENT_LIST) == self.config.event_buffer_size
            ):
                HTTP_EVENT_LIST.pop(0)
            HTTP_EVENT_LIST.append(event)

    async def webhook_event(self, event: Event) -> None:
        """
        处理webhook
        """
        log("DEBUG", "发送webhook...")

        headers = {
            "User-Agent": USER_AGENT,
            "Content-Type": "application/json",
            "X-OneBot-Version": ONEBOT_VERSION,
            "X-Impl": IMPL,
        }
        if self.config.access_token != "":
            headers["Authorization"] = f"Bearer {self.config.access_token}"
        for url in self.config.webhook_url:
            try:
                post_url = URL(url)
                setup = Request(
                    method="POST",
                    url=post_url,
                    headers=headers,
                    json=event.json(
                        by_alias=True, ensure_ascii=False, cls=DataclassEncoder
                    ),
                    timeout=self.config.webhook_timeout / 1000,
                )
                await self.driver.request(setup)
            except Exception as e:
                log("ERROR", f"发送webhook出现错误:{e}")

    async def _send_ws(
        self, ws: Union[FastAPIWebSocket, BackwardWebSocket], event: Event
    ) -> None:
        """
        发送ws消息
        """
        await ws.send(
            event.json(by_alias=True, ensure_ascii=False, cls=DataclassEncoder)
        )

    async def websocket_event(self, event: Event) -> None:
        """
        处理websocket发送事件
        """
        task = [self._send_ws(one, event) for one in self.driver.connects.values()]
        try:
            asyncio.gather(*task)
        except Exception as e:
            log("ERROR", f"发送ws消息出错:{e}")

    async def handle_event(self, event: Event) -> None:
        """
        处理event
        """
        if self.config.enable_http_api:
            asyncio.create_task(self.http_event(event))
        if self.config.enable_http_webhook:
            asyncio.create_task(self.webhook_event(event))
        if self.config.websocekt_type != WebsocketType.Unable:
            asyncio.create_task(self.websocket_event(event))
