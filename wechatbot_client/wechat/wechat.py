from wechatbot_client.action import (
    HttpRequest,
    HttpResponse,
    Request,
    Response,
    check_action_params,
)
from wechatbot_client.config import Config
from wechatbot_client.log import logger

from .api_manager import ApiManager
from .driver import Driver


class WeChatManager:
    """
    微信客户端管理
    """

    config: Config
    """
    应用设置
    """
    api_manager: ApiManager
    """
    api管理模块
    """
    self_id: str
    """自身微信id"""
    driver: Driver
    """后端驱动"""

    def __init__(self, config: Config) -> None:
        self.config = config
        self.driver = Driver(config)
        self.api_manager = ApiManager()
        self.self_id = None

    def init(self) -> None:
        """
        初始化wechat管理端
        """
        self.api_manager.init()

        logger.debug("<y>开始获取wxid...</y>")
        self.self_id = self.api_manager.get_wxid()
        logger.debug("<g>微信id获取成功...</g>")
        logger.info("<g>初始化完成，启动uvicorn...</g>")

    def open_recv_msg(self, file_path: str) -> None:
        """
        开始接收消息
        """
        self.api_manager.open_recv_msg(file_path)

    def close(self) -> None:
        """
        管理微信管理模块
        """
        self.api_manager.close()

    async def _handle_api(self, request: Request) -> Response:
        """
        处理api调用请求
        """
        # 确认action
        try:
            check_action_params(request)
        except TypeError:
            return Response(status=404, msg=f"{request.action} :该功能未实现", data={})
        except ValueError:
            return Response(status=412, msg="请求参数错误", data={})
        # 调用action
        return self.api_manager.request(request)

    async def handle_http_api(self, request: HttpRequest) -> HttpResponse:
        """
        说明:
            处理http_api请求

        参数:
            * `request`：http请求

        返回:
            * `HttpResponse`：http响应
        """
        request = Request(action=request.action, params=request.params)
        response = await self._handle_api(request)
        return HttpResponse(
            status=response.status, msg=response.msg, data=response.data
        )
