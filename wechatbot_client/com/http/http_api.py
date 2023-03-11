"""http_api调用
"""
from fastapi import APIRouter, Body, Response
from pydantic.error_wrappers import ValidationError

from wechatbot_client.action import HttpRequest, HttpResponse
from wechatbot_client.log import logger
from wechatbot_client.utils import escape_tag
from wechatbot_client.wechat import get_wechat

router = APIRouter()


@router.post("/{action}", response_model=HttpResponse)
async def _(action: str, response: Response, params=Body(None)) -> None:
    """处理api调用"""
    # 构造请求体
    logger.info(
        f"<m>http_api</m> - <g>收到http api请求：</g>action：{action}，params：{params}"
    )
    try:
        http_request = HttpRequest(action=action, params=params)
    except ValidationError:
        logger.error("<m>http_api</m> - <r>请求参数不正确!</r>")
        return HttpResponse(status=405, msg="请求参数不正确！", data={})
    wechat_client = get_wechat()
    res = await wechat_client.handle_http_api(http_request)
    response.headers["X-self-ID"] = wechat_client.self_id
    response.headers["access_token"] = wechat_client.config.access_token
    logger.info(f"<m>http_api</m> - <g>调用返回：</g>{escape_tag(str(res))}")

    return res
