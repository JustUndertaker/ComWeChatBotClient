from typing import Any, Literal, Optional

from pydantic import BaseModel, Extra

from wechatbot_client.consts import PLATFORM


class BotSelf(BaseModel):
    """机器人自身"""

    platform: str = PLATFORM
    """消息平台"""
    user_id: str
    """机器人用户 ID"""


class ActionRequest(BaseModel, extra=Extra.forbid):
    """动作请求"""

    action: str
    """请求方法"""
    params: dict
    """请求参数"""
    self: Optional[BotSelf]
    """self参数"""


class WsActionRequest(ActionRequest):
    """ws请求"""

    echo: str
    """ws请求echo"""


class ActionResponse(BaseModel, extra=Extra.forbid):
    """action回复"""

    status: Literal["ok", "failed"]
    """执行状态（成功与否）"""
    retcode: int
    """返回码"""
    data: Any
    """响应数据"""
    message: str = ""
    """错误信息"""


class WsActionResponse(ActionResponse):
    """ws的response"""

    echo: str
    """echo值"""


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
