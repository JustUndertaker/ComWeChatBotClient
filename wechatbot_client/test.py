"""
http_api调用,用来做测试用
"""
from typing import Any, Optional

from fastapi import APIRouter, Body, Response
from pydantic import BaseModel

from wechatbot_client import get_wechat
from wechatbot_client.log import logger
from wechatbot_client.utils import escape_tag

router = APIRouter()


class HttpRequest(BaseModel):
    action: str
    params: Optional[dict]


class HttpResponse(BaseModel):
    status: int
    msg: str
    data: Any


@router.post("/{action}", response_model=HttpResponse)
async def _(action: str, response: Response, params=Body(None)) -> None:
    """处理api调用"""
    # 构造请求体
    logger.info(
        f"<m>http_api</m> - <g>收到http api请求：</g>action：{action}，params：{params}"
    )
    wechat_client = get_wechat()
    if params is None:
        params = {}
    func = getattr(wechat_client.action_manager.com_api, action)
    data = func(**params)
    response.headers["X-self-ID"] = wechat_client.self_id
    response.headers["access_token"] = wechat_client.config.access_token
    logger.info(f"<m>http_api</m> - <g>调用返回：</g>{escape_tag(str(data))}")

    return HttpResponse(status=200, msg="", data=data)
