import time
from pathlib import Path
from uuid import uuid4

from pydantic import ValidationError

from wechatbot_client.action_manager import (
    ActionManager,
    ActionRequest,
    ActionResponse,
    WsActionRequest,
    WsActionResponse,
    check_action_params,
)
from wechatbot_client.com_wechat import Message, MessageHandler
from wechatbot_client.config import Config
from wechatbot_client.consts import FILE_CACHE
from wechatbot_client.file_manager import FileManager
from wechatbot_client.onebot12 import (
    BotSelf,
    BotStatus,
    Event,
    Status,
    StatusUpdateEvent,
)
from wechatbot_client.typing import overrides
from wechatbot_client.utils import logger_wrapper, escape_tag

from .adapter import Adapter

log = logger_wrapper("WeChat Manager")


class WeChatManager(Adapter):
    """
    微信客户端行为管理
    """

    self_id: str
    """自身微信id"""
    file_manager: FileManager
    """文件管理模块"""
    action_manager: ActionManager
    """api管理模块"""
    message_handler: MessageHandler
    """消息处理器"""

    def __init__(self, config: Config) -> None:
        super().__init__(config)
        self.self_id = None
        self.message_handler = None
        self.action_manager = ActionManager()
        self.file_manager = FileManager()

    def init(self) -> None:
        """
        初始化wechat管理端
        """
        self.action_manager.init(self.file_manager, self.config)

        log("DEBUG", "<y>开始获取wxid...</y>")
        info = self.action_manager.get_info()
        self.self_id = info["wxId"]
        video_path = Path(info["wxFilePath"]).parent
        cache_path = Path(f"./{FILE_CACHE}")
        image_path = cache_path / "image" / self.self_id
        voice_path = cache_path / "voice" / self.self_id
        self.message_handler = MessageHandler(
            image_path, voice_path, video_path, self.file_manager
        )
        self.action_manager.register_message_handler(self.handle_msg)
        log("DEBUG", "<g>微信id获取成功...</g>")
        log("INFO", "<g>初始化完成，启动uvicorn...</g>")

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

    @overrides(Adapter)
    async def action_request(self, request: ActionRequest) -> ActionResponse:
        """
        发起action请求
        """
        # 验证action
        try:
            action_name, action_model = check_action_params(request)
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
        return await self.action_manager.request(action_name, action_model)

    @overrides(Adapter)
    def get_status_update_event(slef) -> StatusUpdateEvent:
        """
        获取状态更新事件
        """
        event_id = str(uuid4())
        botself = BotSelf(user_id=slef.self_id)
        botstatus = BotStatus(self=botself, online=True)
        return StatusUpdateEvent(
            id=event_id, time=time.time(), status=Status(good=True, bots=[botstatus])
        )

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

    async def handle_msg(self, msg: str) -> None:
        """
        消息处理函数
        """
        try:
            message = Message.parse_raw(msg)
        except ValidationError as e:
            log("ERROR", f"微信消息实例化失败:{e}")
            return
        if message.isSendMsg:
            await self.handle_self_msg(message)
        else:
            await self.handle_evnt_msg(message)

    async def handle_self_msg(self, msg: Message) -> None:
        """
        处理自身发送消息
        """
        # 先确认是否为自己手动发送
        if msg.isSendByPhone is not None:
            return
        pass

    async def handle_evnt_msg(self, msg: Message) -> None:
        """
        处理event消息
        """
        try:
            event: Event = await self.message_handler.message_to_event(msg)
        except Exception as e:
            log("ERROR", f"生成事件出错:{e}")
            return
        if event is None:
            log("DEBUG", "未生成合适事件")
            return
        log("SUCCESS", f"生成事件<g>[{event.__repr_name__()}]</g>:{escape_tag(format(event.dict()))}")
        await self.handle_event(event)
