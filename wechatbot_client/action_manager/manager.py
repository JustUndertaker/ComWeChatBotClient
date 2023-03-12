import time
from pathlib import Path
from typing import Callable, Literal

from wechatbot_client.com_wechat import ComWechatApi
from wechatbot_client.consts import IMPL, ONEBOT_VERSION, PREFIX, VERSION
from wechatbot_client.log import logger
from wechatbot_client.onebot12 import Message
from wechatbot_client.utils import escape_tag

from .action import ActionRequest, ActionResponse, BotSelf
from .check import add_action, get_supported_actions


class ApiManager:
    """
    api管理器，实现与com交互
    """

    com_api: ComWechatApi
    """com交互api"""

    def __init__(self) -> None:
        self.com_api = ComWechatApi()

    def init(self) -> None:
        """
        初始化com
        """
        # 初始化com组件
        logger.debug("<y>初始化com组件...</y>")
        if not self.com_api.init():
            logger.error("<r>未注册com组件，启动失败...</r>")
            exit(0)
        logger.debug("<g>com组件初始化成功...</g>")
        # 启动微信进程
        logger.debug("<y>正在初始化微信进程...</y>")
        if not self.com_api.init_wechat_pid():
            logger.error("<r>微信进程启动失败...</r>")
            self.com_api.close()
            exit(0)
        logger.debug("<g>找到微信进程...</g>")
        # 注入dll
        logger.debug("<y>正在注入微信...</y>")
        if not self.com_api.start_service():
            logger.error("<r>微信进程启动失败...</r>")
            self.com_api.close()
            exit(0)
        logger.success("<g>dll注入成功...</g>")
        # 等待登录
        logger.info("<y>等待登录...</y>")
        if not self.wait_for_login():
            logger.info("<g>进程关闭...</g>")
            self.com_api.close()
            exit(0)
        logger.success("<g>登录完成...</g>")

    def wait_for_login(self) -> bool:
        """
        等待登录
        """
        while True:
            try:
                if self.com_api.is_wechat_login():
                    return True
                time.sleep(1)
            except KeyboardInterrupt:
                return False

    def open_recv_msg(self, file_path: str) -> None:
        """
        注册接收消息
        """
        # 注册消息事件
        self.com_api.register_msg_event()
        logger.debug("<g>注册消息事件成功...</g>")
        # 启动消息hook
        result = self.com_api.start_receive_message()
        if not result:
            logger.error("<r>启动消息hook失败...</r>")
        logger.debug("<g>启动消息hook成功...</g>")
        # 启动图片hook
        file = Path(file_path)
        img_file = file / "image"
        result = self.com_api.hook_image_msg(str(img_file.absolute()))
        if not result:
            logger.error("<r>启动图片hook失败...</r>")
        logger.debug("<g>启动图片hook成功...</g>")
        # 启动语音hook
        voice_file = file / "voice"
        result = self.com_api.hook_voice_msg(str(voice_file.absolute()))
        if not result:
            logger.error("<r>启动语音hook失败...</r>")
        logger.debug("<g>启动语音hook成功...</g>")

    def close(self) -> None:
        """
        关闭
        """
        self.com_api.close()

    def get_wxid(self) -> str:
        """
        获取wxid
        """
        info = self.com_api.get_self_info()
        return info["wxId"]

    def request(self, request: ActionRequest) -> ActionResponse:
        """
        说明:
            发送action请求，获取返回值

        参数:
            * `request`: action请求体

        返回:
            * `response`: action返回值
        """
        func = getattr(self, request.action)
        try:
            result = func(**request.params)
        except Exception as e:
            logger.error(f"<r>调用api错误: {e}</r>")
            return ActionResponse(status=500, msg="内部服务错误...", data={})
        logger.debug(f"<g>调用api成功，返回:</g> {escape_tag(str(result))}")
        return ActionResponse(status=200, msg="请求成功", data=result)

    def register_message_handler(self, func: Callable[[str], None]) -> None:
        """注册一个消息处理器"""
        self.com_api.register_message_handler(func)


class ActionManager(ApiManager):
    """
    action管理器，实现所有action，这里只定义与com交互的action方法
    """

    @add_action
    def get_supported_actions(self) -> ActionResponse:
        """
        获取支持的动作列表
        """
        actions = get_supported_actions()
        return ActionResponse(status="ok", retcode=0, data=actions)

    @add_action
    def get_status(self) -> ActionResponse:
        """
        获取运行状态
        """
        bot = {"self": BotSelf(user_id=self.get_wxid()).dict(), "online": True}
        data = {"good": True, "bots": [bot]}
        return ActionResponse(status="ok", retcode=0, data=data)

    @add_action
    def get_version(self) -> ActionResponse:
        """
        获取版本信息
        """
        data = {
            "impl": IMPL,
            "version": VERSION,
            "onebot_version": ONEBOT_VERSION,
        }
        return ActionResponse(status="ok", retcode=0, data=data)

    @add_action
    def send_message(
        self,
        detail_type: Literal["private", "group", "channel"],
        message: Message,
        user_id: str = None,
        group_id: str = None,
        guild_id: str = None,
        channel_id: str = None,
    ) -> ActionResponse:
        """
        发送消息
        """
        pass

    @add_action
    def get_self_info(self) -> ActionResponse:
        """
        获取机器人自身信息
        """
        info = self.com_api.get_self_info()
        data = {
            "user_id": info["wxId"],
            "user_name": info["wxNickName"],
            "user_displayname": "",
            f"{PREFIX}.sex": info["Sex"],  # 性别
            f"{PREFIX}.wx_number": info["wxNumber"],  # 微信号
            f"{PREFIX}.avatar": info["wxBigAvatar"],  # 头像
        }
        return ActionResponse(status="ok", retcode=0, data=data)

    @add_action
    def get_user_info(self, user_id: str) -> ActionResponse:
        """
        获取用户信息
        """
        info = self.com_api.get_user_info(user_id)
        data = {
            "user_id": user_id,
            "user_name": info["wxNickName"],
            "user_displayname": "",
            "user_remark": info["wxRemark"],
            f"{PREFIX}.avatar": info["wxBigAvatar"],  # 头像
            f"{PREFIX}.wx_number": info["wxNumber"],  # 微信号
            f"{PREFIX}.nation": info["wxNation"],  # 国家
            f"{PREFIX}.province": info["wxProvince"],  # 省份
            f"{PREFIX}.city": info["wxCity"],  # 城市
            f"{PREFIX}.remark": info["wxRemark"],  # 备注
            f"{PREFIX}.signatrue": info["wxSignature"],  # 个签
            f"{PREFIX}.v3": info["wxV3"],  # v3信息
        }
        return ActionResponse(status="ok", retcode=0, data=data)

    @add_action
    def get_friend_list(self) -> ActionResponse:
        """
        获取好友列表
        """
        res = self.com_api.get_friend_list()
        data = [
            {
                "user_id": one["wxid"],
                "user_name": one["wxNickName"],
                "user_displayname": "",
                "user_remark": one["wxRemark"],
                f"{PREFIX}.verify_flag": one["wxVerifyFlag"],  # 好友标志
            }
            for one in res
        ]
        return ActionResponse(status="ok", retcode=0, data=data)

    @add_action
    def get_group_info(self, group_id: str) -> ActionResponse:
        """
        获取群信息
        """
        info = self.com_api.get_user_info(group_id)
        data = {
            "group_id": info["wxId"],
            "group_name": info["wxNickName"],  # 加入拓展字段
            f"{PREFIX}.avatar": info["wxSmallAvatar"],  # 头像
            f"{PREFIX}.v3": info["wxV3"],  # v3信息
        }
        return ActionResponse(status="ok", retcode=0, data=data)

    @add_action
    def get_group_list(self) -> ActionResponse:
        """
        获取群列表
        """
        res = self.com_api.get_group_list()
        data = [
            {
                "group_id": one["wxId"],
                "group_name": one["wxNickName"],
            }
            for one in res
        ]
        return ActionResponse(status="ok", retcode=0, data=data)

    @add_action
    def get_group_member_info(self, group_id: str, user_id: str) -> ActionResponse:
        """
        获取群成员信息
        """
        res = self.com_api.get_group_members(group_id)
        members = res["members"]
        flag = False
        for one in members:
            if one["wxId"] == user_id:
                data = {
                    "user_id": one["wxId"],
                    "user_name": one["wxNickName"],
                    "user_displayname": "",
                    "user_remark": one["wxRemark"],
                    f"{PREFIX}.avatar": one["wxBigAvatar"],  # 头像
                    f"{PREFIX}.wx_number": one["wxNumber"],  # 微信号
                    f"{PREFIX}.nation": one["wxNation"],  # 国家
                    f"{PREFIX}.province": one["wxProvince"],  # 省份
                    f"{PREFIX}.city": one["wxCity"],  # 城市
                    f"{PREFIX}.remark": one["wxRemark"],  # 备注
                    f"{PREFIX}.signatrue": one["wxSignature"],  # 个签
                    f"{PREFIX}.v3": one["wxV3"],  # v3信息
                }
                flag = True
                break
        if not flag:
            return ActionResponse(
                status="failed", retcode=35001, data=None, message="群内没有该联系人"
            )
        return ActionResponse(status="ok", retcode=0, data=data)

    @add_action
    def get_group_member_list(self, group_id: str) -> ActionResponse:
        """
        获取群成员列表
        """
        res = self.com_api.get_group_members(group_id)
        members = res["members"]
        data = [
            {
                "user_id": one["wxId"],
                "user_name": one["wxNickName"],
                "user_displayname": "",
                "user_remark": one["wxRemark"],
                f"{PREFIX}.avatar": one["wxBigAvatar"],  # 头像
                f"{PREFIX}.wx_number": one["wxNumber"],  # 微信号
                f"{PREFIX}.nation": one["wxNation"],  # 国家
                f"{PREFIX}.province": one["wxProvince"],  # 省份
                f"{PREFIX}.city": one["wxCity"],  # 城市
                f"{PREFIX}.remark": one["wxRemark"],  # 备注
                f"{PREFIX}.signatrue": one["wxSignature"],  # 个签
                f"{PREFIX}.v3": one["wxV3"],  # v3信息
            }
            for one in members
        ]
        return ActionResponse(status="ok", retcode=0, data=data)

    @add_action
    def set_group_name(self, group_id: str, group_name: str) -> ActionResponse:
        """
        设置群名称
        """
        res = self.com_api.set_group_name(group_id, group_name)
        if res:
            return ActionResponse(status="ok", retcode=0, data=None)
        else:
            return ActionResponse(
                status="failed", retcode=35000, data=None, message="操作失败"
            )
