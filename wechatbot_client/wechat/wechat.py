from typing import Callable

from wechatbot_client.action_manager import (
    ActionManager,
    ActionRequest,
    ActionResponse,
    WsActionRequest,
    WsActionResponse,
    check_action_params,
)
from wechatbot_client.config import Config
from wechatbot_client.log import logger
from wechatbot_client.typing import overrides

from .adapter import Adapter


class WeChatManager(Adapter):
    """
    微信客户端行为管理
    """

    action_manager: ActionManager
    """api管理模块"""
    self_id: str
    """自身微信id"""

    def __init__(self, config: Config) -> None:
        super().__init__(config)
        self.action_manager = ActionManager()
        self.self_id = None

    def init(self) -> None:
        """
        初始化wechat管理端
        """
        self.action_manager.init()

        logger.debug("<y>开始获取wxid...</y>")
        self.self_id = self.action_manager.get_wxid()
        logger.debug("<g>微信id获取成功...</g>")
        logger.info("<g>初始化完成，启动uvicorn...</g>")

    def open_recv_msg(self, file_path: str) -> None:
        """
        开始接收消息
        """
        self.action_manager.open_recv_msg(file_path)

    def close(self) -> None:
        """
        管理微信管理模块
        """
        self.action_manager.close()

    def register_message_handler(self, func: Callable[[str], None]) -> None:
        """
        注册一个消息处理器
        """
        self.action_manager.register_message_handler(func)

    @overrides(Adapter)
    async def action_request(self, request: ActionRequest) -> ActionResponse:
        """
        发起action请求
        """
        # 验证action
        try:
            check_action_params(request)
        except TypeError:
            return ActionResponse(
                status="failed",
                retcode=10002,
                data=None,
                message=f"未实现的action: {request.action}",
            )
        except ValueError:
            return ActionResponse(
                status="failed",
                retcode=10003,
                data=None,
                message="Param参数错误",
            )
        # 调用api
        return self.action_manager.request(request)

    @overrides(Adapter)
    async def action_ws_request(self, request: WsActionRequest) -> WsActionResponse:
        """
        处理ws请求
        """
        echo = request.echo
        response = await self.action_request(
            ActionRequest(action=request.action, params=request.params)
        )
        return WsActionResponse(echo=echo, **response.dict())
