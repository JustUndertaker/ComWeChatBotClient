from typing import Any, Optional

from pydantic import BaseModel


class Request(BaseModel):
    """api 请求基类"""

    action: str
    """请求方法"""
    params: Optional[dict]
    """请求参数"""


class HttpRequest(Request):
    """请求体参数"""

    ...


class WsRequest(Request):
    """websocket api 请求"""

    echo: str
    """echo值"""


class Response(BaseModel):
    """api 响应基类"""

    status: int
    """状态值"""
    msg: str
    """回复消息"""
    data: Any
    """返回数据"""


class HttpResponse(Response):
    """http api 响应"""

    ...


class WsResponse(Response):
    """websocket api 响应"""

    echo: str
    """echo值"""
