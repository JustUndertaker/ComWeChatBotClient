import time
from base64 import b64decode
from inspect import iscoroutinefunction
from pathlib import Path
from sys import exit
from typing import Callable, Literal, Optional, ParamSpec, TypeVar, Union

from pydantic import BaseModel

from wechatbot_client.com_wechat import ComWechatApi
from wechatbot_client.config import Config
from wechatbot_client.consts import IMPL, ONEBOT_VERSION, PREFIX, VERSION
from wechatbot_client.exception import FileNotFound, NoThisUserInGroup
from wechatbot_client.file_manager import FileCache, FileManager
from wechatbot_client.onebot12 import Message, MessageSegment
from wechatbot_client.utils import escape_tag, logger_wrapper

from .check import expand_action, get_supported_actions, standard_action
from .model import ActionResponse, BotSelf

log = logger_wrapper("Action Manager")
P = ParamSpec("P")
R = TypeVar("R")

SEGMENT_HANDLER: dict[str, Callable[P, R]] = {}
"""消息段处理函数"""


def add_segment_handler(_type: str) -> Callable[P, R]:
    """
    添加消息段处理函数
    """

    def _handler(func: Callable[P, R]) -> Callable[P, R]:
        global SEGMENT_HANDLER
        SEGMENT_HANDLER[_type] = func
        return func

    return _handler


class ApiManager:
    """
    api管理器，实现与com交互
    """

    com_api: ComWechatApi
    """com交互api"""
    file_manager: FileManager
    """文件管理器"""
    file_base_url: str
    """文件base url"""

    def __init__(self) -> None:
        self.com_api = ComWechatApi()
        self.file_manager = None

    def init(self, file_manager: FileManager, config: Config) -> None:
        """
        初始化com
        """
        self.file_manager = file_manager
        self.file_base_url = f"http://{config.host}:{config.port}/get_file/"
        # 初始化com组件
        log("DEBUG", "<y>初始化com组件...</y>")
        if not self.com_api.init():
            log("ERROR", "<r>未安装com组件，启动失败，请使用目录下`install.bat`安装组件...</r>")
            exit(0)
        log("DEBUG", "<g>com组件初始化成功...</g>")
        # 启动微信进程
        log("DEBUG", "<y>正在初始化微信进程...</y>")
        if not self.com_api.init_wechat_pid():
            log("ERROR", "<r>微信进程启动失败...</r>")
            self.com_api.close()
            exit(0)
        log("DEBUG", "<g>找到微信进程...</g>")
        # 注入dll
        log("DEBUG", "<y>正在注入微信...</y>")
        if not self.com_api.start_service():
            log("ERROR", "<r>微信进程启动失败...</r>")
            self.com_api.close()
            exit(0)
        log("SUCCESS", "<g>dll注入成功...</g>")
        # 等待登录
        log("INFO", "<y>等待登录...</y>")
        if not self.wait_for_login():
            log("INFO", "<g>进程关闭...</g>")
            self.com_api.close()
            exit(0)
        log("SUCCESS", "<g>登录完成...</g>")

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
        log("DEBUG", "<g>注册消息事件成功...</g>")
        # 启动消息hook
        result = self.com_api.start_receive_message()
        if not result:
            log("ERROR", "<r>启动消息hook失败...</r>")
        log("DEBUG", "<g>启动消息hook成功...</g>")
        # 启动图片hook
        file = Path(file_path)
        img_file = file / "image"
        result = self.com_api.hook_image_msg(str(img_file.absolute()))
        if not result:
            log("ERROR", "<r>启动图片hook失败...</r>")
        log("DEBUG", "<g>启动图片hook成功...</g>")
        # 启动语音hook
        voice_file = file / "voice"
        result = self.com_api.hook_voice_msg(str(voice_file.absolute()))
        if not result:
            log("ERROR", "<r>启动语音hook失败...</r>")
        log("DEBUG", "<g>启动语音hook成功...</g>")

    def close(self) -> None:
        """
        关闭
        """
        self.com_api.close()

    def get_info(self) -> dict:
        """
        获取自身信息
        """
        return self.com_api.get_self_info()

    async def request(
        self, action_name: str, action_model: BaseModel
    ) -> ActionResponse:
        """
        说明:
            发送action请求，获取返回值

        参数:
            * `action_name`: action请求函数名
            * `action_model`: action参数模型

        返回:
            * `response`: action返回值
        """
        func = getattr(self, action_name)
        try:
            if iscoroutinefunction(func):
                result = await func(**action_model.dict())
            else:
                result = func(**action_model.dict())
        except Exception as e:
            log("ERROR", f"<r>调用api错误: {e}</r>")
            return ActionResponse(
                status="failed", retcode=20002, message="内部服务错误", data=None
            )
        log("DEBUG", f"<g>调用api成功，返回:</g> {escape_tag(str(result))}")
        return result

    def register_message_handler(self, func: Callable[[str], None]) -> None:
        """注册一个消息处理器"""
        self.com_api.register_message_handler(func)

    @add_segment_handler("text")
    def _send_text(
        self, id: str, segment: MessageSegment, at_list: list[str] = None
    ) -> bool:
        """
        发送文本
        """
        if at_list is None:
            return self.com_api.send_text(wxid=id, message=segment.data["text"])
        else:
            return self.com_api.send_at_message(
                group_id=id,
                at_users=at_list,
                message=segment.data["text"],
                auto_nickname=False,
            )

    @add_segment_handler("image")
    async def _send_image(self, id: str, segment: MessageSegment) -> bool:
        """发送图片"""
        file_id = segment.data["file_id"]
        file_path, _ = await self.file_manager.get_file(file_id)
        if file_path is None:
            raise FileNotFound(file_id)
        return self.com_api.send_image(id, file_path)

    @add_segment_handler("file")
    async def _send_file(self, id: str, segment: MessageSegment) -> bool:
        """发送文件"""
        file_id = segment.data["file_id"]
        file_path, _ = await self.file_manager.get_file(file_id)
        if file_path is None:
            raise FileNotFound(file_id)
        return self.com_api.send_file(id, file_path)

    @add_segment_handler(f"{PREFIX}.emoji")
    async def _send_emoji(self, id: str, segment: MessageSegment) -> bool:
        """发送gif表情"""
        file_id = segment.data["file_id"]
        file_path, _ = await self.file_manager.get_file(file_id)
        if file_path is None:
            raise FileNotFound(file_id)
        return self.com_api.send_gif(id, file_path)

    @add_segment_handler(f"{PREFIX}.link")
    async def _send_link(self, id: str, segment: MessageSegment) -> bool:
        """
        发送链接消息
        """
        file_id = segment.data.get("file_id")
        file_path = None
        if file_id is not None:
            file_path, _ = await self.file_manager.get_file(file_id)
        title = segment.data["title"]
        des = segment.data["des"]
        url = segment.data["url"]
        return self.com_api.send_message_card(id, title, des, url, file_path)


class ActionManager(ApiManager):
    """
    action管理器，实现所有action
    """

    @standard_action
    def get_supported_actions(self) -> ActionResponse:
        """
        获取支持的动作列表
        """
        actions = get_supported_actions()
        return ActionResponse(status="ok", retcode=0, data=actions)

    @standard_action
    def get_status(self) -> ActionResponse:
        """
        获取运行状态
        """
        user_info = self.get_self_info()
        bot = {
            "self": BotSelf(user_id=user_info.data["user_id"]).dict(),
            "online": True,
        }
        data = {"good": True, "bots": [bot]}
        return ActionResponse(status="ok", retcode=0, data=data)

    @standard_action
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

    @standard_action
    async def send_message(
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
        match detail_type:
            case "channel":
                return ActionResponse(
                    status="failed", retcode=10004, data=None, message="不支持channel发送"
                )
            case "private":
                if user_id is None:
                    return ActionResponse(
                        status="failed", retcode=10003, data=None, message="参数缺失"
                    )
                return await self._send_private_msg(message, user_id)
            case "group":
                if group_id is None:
                    return ActionResponse(
                        status="failed", retcode=10003, data=None, message="参数缺失"
                    )
                return await self._send_group_msg(message, group_id)

    def _pre_handle_msg(
        self, group_id: str, message: Message
    ) -> tuple[list[list[str]], Message]:
        """
        消息预处理，将at合并到text中
        """
        new_msg = Message()
        all_at_list: list[list[str]] = []
        current_text = None
        curren_at_list = None
        for segment in message:
            if segment.type == "text":
                current_text = segment
                curren_at_list = []
                new_msg.append(segment)
            elif segment.type == "mention":
                user_id = segment.data["user_id"]
                nickname = self.com_api.get_groupmember_nickname(group_id, user_id)
                if nickname == "":
                    raise NoThisUserInGroup(group_id, user_id)
                seg = MessageSegment.text(f"@{nickname} ")
                new_msg.append(seg)
                if current_text is None:
                    current_text = seg
                    curren_at_list = []
                curren_at_list.append(user_id)
            elif segment.type == "mention_all":
                seg = MessageSegment.text("@全体成员 ")
                new_msg.append(seg)
                if current_text is None:
                    current_text = seg
                    curren_at_list = []
                curren_at_list.append("notify@all")
            else:
                new_msg.append(segment)
                if current_text is not None:
                    if curren_at_list:
                        all_at_list.append(curren_at_list)
                    current_text = None
                    curren_at_list = None
        if current_text is not None:
            if curren_at_list:
                all_at_list.append(curren_at_list)
        new_msg.ruduce()
        return all_at_list, new_msg

    async def _send_private_msg(self, message: Message, user_id: str) -> ActionResponse:
        """
        发送私聊消息
        """
        exceptions: list[str] = []
        for segment in message:
            try:
                if segment.type == "mention" or segment.type == "mention_all":
                    exceptions.append(f"私聊不支持的消息段:{segment.type}")
                    continue
                handler = SEGMENT_HANDLER.get(segment.type)
                if handler is None:
                    exceptions.append(f"不支持的消息段:{segment.type}")
                    continue
                if iscoroutinefunction(handler):
                    await handler(self, user_id, segment)
                else:
                    handler(self, user_id, segment)
            except FileNotFound as e:
                log("ERROR", repr(e))
                exceptions.append("无效的file_id")
                continue
            except Exception as e:
                log("ERROR", "发送消息出错", e)
                exceptions.append(f"发送消息出错:{str(e)}")
                continue
        if exceptions:
            msg = "发送消息时出现以下错误:\n"
            msg += "\n".join(exceptions)
            return ActionResponse(
                status="failed", retcode=10002, data=None, message=msg
            )
        return ActionResponse(status="ok", retcode=0, data=None)

    async def _send_group_msg(self, message: Message, group_id: str) -> ActionResponse:
        """
        发送群消息
        """
        exceptions: list[str] = []
        try:
            all_at_list, message = self._pre_handle_msg(group_id, message)
        except NoThisUserInGroup as e:
            log("ERROR", repr(e))
            return ActionResponse(
                status="failed", retcode=10006, message=repr(e), data=None
            )
        for segment in message:
            try:
                handler = SEGMENT_HANDLER.get(segment.type)
                if handler is None:
                    exceptions.append(f"不支持的消息段:{segment.type}")
                    continue
                if segment.type == "text":
                    if len(all_at_list) == 0:
                        at_list = None
                    else:
                        at_list = all_at_list.pop(0)
                    handler(self, group_id, segment, at_list)
                elif iscoroutinefunction(handler):
                    await handler(self, group_id, segment)
                else:
                    handler(self, group_id, segment)
            except FileNotFound as e:
                log("ERROR", repr(e))
                exceptions.append("无效的file_id")
                continue
            except Exception as e:
                log("ERROR", "发送消息出错", e)
                exceptions.append(f"发送消息出错:{str(e)}")
                continue
        if exceptions:
            msg = "发送消息时出现以下错误:\n"
            msg += "\n".join(exceptions)
            return ActionResponse(
                status="failed", retcode=10002, data=None, message=msg
            )
        return ActionResponse(status="ok", retcode=0, data=None)

    @standard_action
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

    @standard_action
    def get_user_info(self, user_id: str) -> ActionResponse:
        """
        获取用户信息
        """
        info = self.com_api.get_user_info(user_id)
        data = {
            "user_id": user_id,
            "user_name": info["wxNickName"],
            "user_displayname": "",
            "user_remark": info["wxRemark"] if info["wxRemark"] != "null" else "",
            f"{PREFIX}.avatar": info["wxBigAvatar"],  # 头像
            f"{PREFIX}.wx_number": info["wxNumber"],  # 微信号
            f"{PREFIX}.nation": info["wxNation"],  # 国家
            f"{PREFIX}.province": info["wxProvince"],  # 省份
            f"{PREFIX}.city": info["wxCity"],  # 城市
        }
        return ActionResponse(status="ok", retcode=0, data=data)

    @standard_action
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

    @standard_action
    def get_group_info(self, group_id: str) -> ActionResponse:
        """
        获取群信息
        """
        info = self.com_api.get_user_info(group_id)
        data = {
            "group_id": info["wxId"],
            "group_name": info["wxNickName"]
            if info["wxNickName"] != "null"
            else "",  # 加入拓展字段
            f"{PREFIX}.avatar": info["wxSmallAvatar"],  # 头像
        }
        return ActionResponse(status="ok", retcode=0, data=data)

    @standard_action
    def get_group_list(self) -> ActionResponse:
        """
        获取群列表
        """
        res = self.com_api.get_group_list()
        data = [
            {
                "group_id": one["wxid"],
                "group_name": one["wxNickName"],
            }
            for one in res
        ]
        return ActionResponse(status="ok", retcode=0, data=data)

    @standard_action
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
                    f"{PREFIX}.avatar": one["wxBigAvatar"],  # 头像
                    f"{PREFIX}.wx_number": one["wxNumber"],  # 微信号
                    f"{PREFIX}.nation": one["wxNation"],  # 国家
                    f"{PREFIX}.province": one["wxProvince"],  # 省份
                    f"{PREFIX}.city": one["wxCity"],  # 城市
                }
                flag = True
                break
        if not flag:
            return ActionResponse(
                status="failed", retcode=35001, data=None, message="群内没有该联系人"
            )
        return ActionResponse(status="ok", retcode=0, data=data)

    @standard_action
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
                f"{PREFIX}.avatar": one["wxBigAvatar"],  # 头像
                f"{PREFIX}.wx_number": one["wxNumber"],  # 微信号
                f"{PREFIX}.nation": one["wxNation"],  # 国家
                f"{PREFIX}.province": one["wxProvince"],  # 省份
                f"{PREFIX}.city": one["wxCity"],  # 城市
            }
            for one in members
        ]
        return ActionResponse(status="ok", retcode=0, data=data)

    @standard_action
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

    @standard_action
    async def upload_file(
        self,
        type: Literal["url", "path", "data"],
        name: str,
        url: Optional[str] = None,
        headers: Optional[dict[str, str]] = None,
        path: Optional[str] = None,
        data: Optional[Union[str, bytes]] = None,
        sha256: Optional[str] = None,
    ) -> ActionResponse:
        """
        上传文件
        """
        if type == "url":
            if url is None:
                return ActionResponse(
                    status="failed", retcode=10003, data=None, message="缺少url参数"
                )
            file_id = await self.file_manager.cache_file_id_from_url(url, name, headers)
            if file_id is None:
                return ActionResponse(
                    status="failed", retcode=33000, data=None, message="下载文件失败"
                )
            return ActionResponse(status="ok", retcode=0, data={"file_id": file_id})
        if type == "path":
            if path is None:
                return ActionResponse(
                    status="failed", retcode=10003, data=None, message="缺少path参数"
                )
            file_id = await self.file_manager.cache_file_id_from_path(
                Path(path), name=name, copy=False
            )
            if file_id is None:
                return ActionResponse(
                    status="failed", retcode=32000, data=None, message="操作文件失败"
                )
            return ActionResponse(status="ok", retcode=0, data={"file_id": file_id})
        if data is None:
            return ActionResponse(
                status="failed", retcode=10003, data=None, message="缺少data参数"
            )
        if isinstance(data, str):
            data = b64decode(data)
        file_id = await self.file_manager.cache_file_id_from_data(data, name)
        return ActionResponse(status="ok", retcode=0, data={"file_id": file_id})

    @standard_action
    async def get_file(
        self, file_id: str, type: Literal["url", "path", "data"]
    ) -> ActionResponse:
        """
        获取文件
        """
        file_path, file_name = await self.file_manager.get_file(file_id)
        if file_path is None:
            return ActionResponse(
                status="failed", retcode=32000, data=None, message="未找到该文件"
            )
        if type == "url":
            file_id, file_name = await FileCache.get_file(file_id)
            if file_id is None:
                return ActionResponse(
                    status="failed", retcode=32000, data=None, message="未找到该文件"
                )
            url = self.file_base_url + file_id
            return ActionResponse(
                status="ok", retcode=0, data={"name": file_name, "url": url}
            )
        if type == "path":
            return ActionResponse(
                status="ok", retcode=0, data={"name": file_name, "path": file_path}
            )
        with open(file_path, mode="rb") as f:
            data = f.read()
        return ActionResponse(
            status="ok", retcode=0, data={"name": file_name, "data": data}
        )

    @expand_action
    def get_public_account_list(self) -> ActionResponse:
        """
        获取公众号列表
        """
        res = self.com_api.get_public_account_list()
        data = [
            {
                "user_id": one["wxid"],
                "user_name": one["wxNickName"],
                "wx_number": one["wxNumber"],
            }
            for one in res
        ]
        return ActionResponse(status="ok", retcode=0, data=data)

    @expand_action
    def follow_public_number(self, user_id: str) -> ActionResponse:
        """
        说明:
            关注公众号

        参数:
            * `user_id`: 公众号id
        """
        status = self.com_api.follow_public_number(user_id)
        if status:
            return ActionResponse(status="ok", retcode=0, data=None)
        else:
            return ActionResponse(
                status="failed", retcode=35000, data=None, message="操作失败"
            )

    @expand_action
    def search_contact_by_remark(self, remark: str) -> ActionResponse:
        """
        通过备注搜索联系人
        """
        info = self.com_api.search_friend_by_remark(remark)
        if info is None:
            return ActionResponse(
                status="failed", retcode=35001, data=None, message="未找到联系人"
            )
        data = {
            "user_id": info["wxId"],
            "user_name": info["wxNickName"],
            "user_displayname": "",
            "user_remark": info["wxRemark"],
            f"{PREFIX}.avatar": info["wxBigAvatar"],  # 头像
            f"{PREFIX}.wx_number": info["wxNumber"],  # 微信号
            f"{PREFIX}.nation": info["wxNation"],  # 国家
            f"{PREFIX}.province": info["wxProvince"],  # 省份
            f"{PREFIX}.city": info["wxCity"],  # 城市
        }
        return ActionResponse(status="ok", retcode=0, data=data)

    @expand_action
    def search_contact_by_wxnumber(self, wx_number: str) -> ActionResponse:
        """
        通过微信号搜索联系人
        """
        info = self.com_api.search_friend_by_wxnumber(wx_number)
        if info is None:
            return ActionResponse(
                status="failed", retcode=35001, data=None, message="未找到联系人"
            )
        data = {
            "user_id": info["wxId"],
            "user_name": info["wxNickName"],
            "user_displayname": "",
            "user_remark": info["wxRemark"],
            f"{PREFIX}.avatar": info["wxBigAvatar"],  # 头像
            f"{PREFIX}.wx_number": info["wxNumber"],  # 微信号
            f"{PREFIX}.nation": info["wxNation"],  # 国家
            f"{PREFIX}.province": info["wxProvince"],  # 省份
            f"{PREFIX}.city": info["wxCity"],  # 城市
        }
        return ActionResponse(status="ok", retcode=0, data=data)

    @expand_action
    def search_contact_by_nickname(self, nickname: str) -> ActionResponse:
        """
        通过昵称搜索联系人
        """
        info = self.com_api.search_friend_by_nickname(nickname)
        if info is None:
            return ActionResponse(
                status="failed", retcode=35001, data=None, message="未找到联系人"
            )
        data = {
            "user_id": info["wxId"],
            "user_name": info["wxNickName"],
            "user_displayname": "",
            "user_remark": info["wxRemark"],
            f"{PREFIX}.avatar": info["wxBigAvatar"],  # 头像
            f"{PREFIX}.wx_number": info["wxNumber"],  # 微信号
            f"{PREFIX}.nation": info["wxNation"],  # 国家
            f"{PREFIX}.province": info["wxProvince"],  # 省份
            f"{PREFIX}.city": info["wxCity"],  # 城市
        }
        return ActionResponse(status="ok", retcode=0, data=data)

    @expand_action
    def check_friend_status(self, user_id: str) -> ActionResponse:
        """
        说明:
            检测好友状态

        参数:
            * `wxid`: 好友wxid

        返回:
            * `int`: 好友状态
                * `0x00`: Unknown
                * `0xB0`: 被删除
                * `0xB1`: 是好友
                * `0xB2`: 已拉黑
                * `0xB5`: 被拉黑
        """
        data = self.com_api.check_friend_status(user_id)
        return ActionResponse(status="ok", retcode=0, data=data)

    @expand_action
    def get_db_info(self) -> ActionResponse:
        """
        获取数据库句柄和表信息
        """
        data = self.com_api.get_db_handles()
        return ActionResponse(status="ok", retcode=0, data=data)

    @expand_action
    def execute_sql(self, handle: int, sql: str) -> ActionResponse:
        """
        执行SQL
        """
        data = self.com_api.execute_sql(handle, sql)
        return ActionResponse(status="ok", retcode=0, data=data)

    @expand_action
    def backup_db(self, handle: int, file_path: str) -> ActionResponse:
        """
        备份数据库
        """
        status = self.com_api.backup_db(handle, file_path)
        if status:
            return ActionResponse(status="ok", retcode=0, data=None)
        else:
            return ActionResponse(
                status="failed", retcode=32000, data=None, message="备份数据库失败"
            )

    @expand_action
    def accept_friend(self, v3: str, v4: str) -> ActionResponse:
        """
        说明:
            通过好友请求

        参数:
            * `v3`: v3数据(encryptUserName)
            * `v4`: v4数据(ticket)
        """
        status = self.com_api.verify_friend_apply(v3, v4)
        if status:
            return ActionResponse(status="ok", retcode=0, data=None)
        else:
            return ActionResponse(
                status="failed", retcode=35000, data=None, message="操作失败"
            )

    @expand_action
    def get_wechat_version(self) -> ActionResponse:
        """
        获取微信版本
        """
        data = self.com_api.get_wechat_version()
        return ActionResponse(status="ok", retcode=0, data=data)

    @expand_action
    def set_wechat_version(self, version: str) -> ActionResponse:
        """
        说明:
            自定义微信版本号，一定程度上防止自动更新

        参数:
            * `version`: 版本号，类似`3.7.0.26`
        """
        status = self.com_api.change_wechat_version(version)
        if status:
            return ActionResponse(status="ok", retcode=0, data=None)
        else:
            return ActionResponse(
                status="failed", retcode=35000, data=None, message="操作失败"
            )

    @expand_action
    def delete_friend(self, user_id: str) -> ActionResponse:
        """
        删除好友
        """
        status = self.com_api.delete_friend(user_id)
        if status:
            self.com_api.get_contacts()
            return ActionResponse(status="ok", retcode=0, data=None)
        else:
            return ActionResponse(
                status="failed", retcode=35000, data=None, message="操作失败"
            )

    @expand_action
    def set_remark(self, user_id: str, remark: str) -> ActionResponse:
        """
        说明:
            修改好友或群聊备注

        参数:
            * `user_id`: wxid或group_id
            * `remark`: 要修改的备注
        """
        status = self.com_api.edit_remark(user_id, remark)
        if status:
            self.com_api.get_contacts()
            return ActionResponse(status="ok", retcode=0, data=None)
        else:
            return ActionResponse(
                status="failed", retcode=35000, data=None, message="操作失败"
            )

    @expand_action
    def set_group_announcement(
        self, group_id: str, announcement: str
    ) -> ActionResponse:
        """
        设置群公告.请确认具有相关权限再调用。
        """
        status = self.com_api.set_group_announcement(group_id, announcement)
        if status:
            self.com_api.get_contacts()
            return ActionResponse(status="ok", retcode=0, data=None)
        else:
            return ActionResponse(
                status="failed", retcode=35000, data=None, message="操作失败"
            )

    @expand_action
    def set_group_nickname(self, group_id: str, nickname: str) -> ActionResponse:
        """
        说明:
            设置群昵称
        """
        status = self.com_api.set_group_nickname(group_id, nickname)
        if status:
            self.com_api.get_contacts()
            return ActionResponse(status="ok", retcode=0, data=None)
        else:
            return ActionResponse(
                status="failed", retcode=35000, data=None, message="操作失败"
            )

    @expand_action
    def get_groupmember_nickname(self, group_id: str, user_id: str) -> ActionResponse:
        """
        说明:
            获取群成员昵称
        """
        nickname = self.com_api.get_groupmember_nickname(group_id, user_id)
        return ActionResponse(status="ok", retcode=0, data=nickname)

    @expand_action
    def delete_groupmember(
        self, group_id: str, user_list: Union[str, list[str]]
    ) -> ActionResponse:
        """
        说明:
            删除群成员.请确认具有相关权限再调用。

        参数:
            * `group_id`: 群聊id
            * `user_list`: 要删除的成员wxid或wxid列表
        """
        status = self.com_api.delete_groupmember(group_id, user_list)
        if status:
            self.com_api.get_contacts()
            return ActionResponse(status="ok", retcode=0, data=None)
        else:
            return ActionResponse(
                status="failed", retcode=35000, data=None, message="操作失败"
            )

    @expand_action
    def add_groupmember(
        self, group_id: str, user_list: Union[str, list[str]]
    ) -> ActionResponse:
        """
        说明:
            添加群成员.请确认具有相关权限再调用。

        参数:
            * `group_id`: 群聊id
            * `user_list`: 要添加的成员wxid或wxid列表
        """
        status = self.com_api.add_groupmember(group_id, user_list)
        if status:
            self.com_api.get_contacts()
            return ActionResponse(status="ok", retcode=0, data=None)
        else:
            return ActionResponse(
                status="failed", retcode=35000, data=None, message="操作失败"
            )

    @expand_action
    def get_public_history(self, public_id: str, offset: str = "") -> ActionResponse:
        """
        说明:
            获取公众号历史消息，一次获取十条推送记录

        参数:
            * `public_id`: 公众号id
            * `offset`: 起始偏移，为空的话则从新到久获取十条，该值可从返回数据中取得. The default is ""
        """
        data = self.com_api.get_history_public_msg(public_id, offset)
        return ActionResponse(status="ok", retcode=0, data=data)

    @expand_action
    def send_forward_msg(self, user_id: str, message_id: int) -> ActionResponse:
        """
        说明:
            转发消息，只支持单条转发

        参数:
            * `wxid`: 消息接收人wxid
            * `message_id`: 消息id，可以在实时消息接口中获取.
        """
        status = self.com_api.send_forward_msg(user_id, message_id)
        if status:
            self.com_api.get_contacts()
            return ActionResponse(status="ok", retcode=0, data=None)
        else:
            return ActionResponse(
                status="failed", retcode=35000, data=None, message="操作失败"
            )

    @expand_action
    def send_raw_xml(
        self, user_id: str, xml: str, image_path: str = ""
    ) -> ActionResponse:
        """
        说明:
            发送原始xml消息

        参数:
            * `user_id`: 消息接收人
            * `xml`: xml内容
            * `image_path`: 图片路径. 默认为空.
        """
        status = self.com_api.send_xml(user_id, xml, image_path)
        if status:
            self.com_api.get_contacts()
            return ActionResponse(status="ok", retcode=0, data=None)
        else:
            return ActionResponse(
                status="failed", retcode=35000, data=None, message="操作失败"
            )

    @expand_action
    def send_card(self, user_id: str, card_id: str, nickname: str) -> ActionResponse:
        """
        发送名片
        """
        status = self.com_api.send_contact_card(user_id, card_id, nickname)
        if status:
            self.com_api.get_contacts()
            return ActionResponse(status="ok", retcode=0, data=None)
        else:
            return ActionResponse(
                status="failed", retcode=35000, data=None, message="操作失败"
            )

    @expand_action
    async def clean_cache(self, days: int = 3) -> ActionResponse:
        """
        说明:
            清理文件缓存

        参数:
            * `days`: 保留天数. 默认为3天.
        """
        nums = await self.file_manager.clean_cache(days)
        return ActionResponse(status="ok", retcode=0, data=nums)
