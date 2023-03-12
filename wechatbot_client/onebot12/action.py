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
