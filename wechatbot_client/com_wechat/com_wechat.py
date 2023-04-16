import asyncio
import json
from pathlib import Path
from typing import Callable, Literal, Optional, Tuple, Union

import psutil
from comtypes.client import CreateObject, GetEvents

from wechatbot_client.utils import escape_tag, logger_wrapper

log = logger_wrapper("Com WeChat")


class MessageReporter:
    """
    消息接收器
    """

    func: Callable[[str], None] = None
    """消息处理器"""

    def OnGetMessageEvent(self, message: Tuple[str, None]):
        msg = message[0]
        log("DEBUG", f"<g>接收到wechat消息</g> - {escape_tag(msg)}")
        if self.func:
            asyncio.create_task(self.func(msg))

    def register_message_handler(self, func: Callable[[str], None]) -> None:
        """注册一个消息处理器"""
        self.func = func


class ComProgress:
    """
    com通讯组件
    """

    robot = None
    """com通讯robot"""
    event = None
    """com通讯event"""
    com_pid: int
    """com进程的pid"""
    wechat_pid: int
    """微信pid"""
    connection_point = None
    """消息接收点"""
    msg_reporter: MessageReporter
    """消息接收器"""

    def __init__(self) -> None:
        self.robot = None
        self.event = None
        self.com_pid = None
        self.wechat_pid = None
        self.connection_point = None
        self.msg_reporter = MessageReporter()

    def init(self) -> bool:
        """
        初始化com组件
        """
        try:
            self.robot = CreateObject("WeChatRobot.CWeChatRobot")
            self.event = CreateObject("WeChatRobot.RobotEvent")
            self.com_pid = self.robot.CStopRobotService(0)
        except OSError:
            return False
        return True

    def close(self) -> None:
        """
        关闭com进程
        """
        if self.com_pid is not None:
            try:
                com_process = psutil.Process(self.com_pid)
                com_process.kill()
            except psutil.NoSuchProcess:
                pass
        self.com_pid = None

    def register_msg_event(self) -> None:
        """
        注册消息事件
        """
        self.connection_point = GetEvents(self.event, self.msg_reporter)
        self.event.CRegisterWxPidWithCookie(
            self.wechat_pid, self.connection_point.cookie
        )

    def register_message_handler(self, func: Callable[[str], None]) -> None:
        """注册一个消息处理器"""
        self.msg_reporter.register_message_handler(func)


class ComWechatApi(ComProgress):
    """
    com微信通信接口，继承ComProgress，这里只定义方法
    """

    AddressBook: list[dict] = None
    """通讯录列表"""

    def init_wechat_pid(self) -> bool:
        """
        说明:
            初始化微信，并获取pid

        返回:
            是否成功
        """
        # 查找已开微信进程
        pid_list = []
        process_list = psutil.pids()
        for pid in process_list:
            try:
                if psutil.Process(pid).name() == "WeChat.exe":
                    pid_list.append(pid)
            except psutil.NoSuchProcess:
                pass
        if pid_list:
            self.wechat_pid = pid_list[0]
            return True
        # 自己启动微信
        pid = self.start_wechat()
        if pid != 0:
            self.wechat_pid = pid
            return True
        return False

    def start_wechat(self) -> int:
        """
        说明:
            启动微信

        返回:
            * `int`: 微信pid，为0则失败
        """
        return self.robot.CStartWeChat()

    def start_service(self) -> bool:
        """
        说明:
            注入DLL到微信以启动服务

        返回:
            * `bool`: 操作是否成功
        """
        status = self.robot.CStartRobotService(self.wechat_pid)
        return status == 0

    def stop_service(self) -> int:
        """
        说明:
            停止服务，会将DLL从微信进程中卸载

        返回:
            * `int`: COM进程pid.
        """

        com_pid = self.robot.CStopRobotService(self.wechat_pid)
        return com_pid

    def is_wechat_login(self) -> bool:
        """
        说明:
            获取微信登录状态

        返回:
            * `bool`: 微信登录状态
        """

        status = self.robot.CIsWxLogin(self.wechat_pid)
        return status == 1

    def send_text(self, wxid: str, message: str) -> bool:
        """
        说明:
            发送文本消息

        参数:
            * `wxid`: 对方wxid
            * `message`: 要发送的内容

        返回:
            * `bool`: 操作是否成功
        """

        status = self.robot.CSendText(self.wechat_pid, wxid, message)
        return status == 0

    def send_image(self, wxid: str, image_path: str) -> bool:
        """
        说明:
            发送图片消息

        参数:
            * `wxid`: 对方wxid
            * `image_path`: 图片绝对路径

        返回:
            * `bool`: 发送是否成功
        """

        status = self.robot.CSendImage(self.wechat_pid, wxid, image_path)
        return status == 0

    def send_file(self, wxid: str, file_path: str) -> bool:
        """
        说明:
            发送文件

        参数:
            * `wxid`: 对方wxid
            * `file_path`: 文件绝对路径

        返回:
            * `bool`: 发送是否成功
        """

        status = self.robot.CSendFile(self.wechat_pid, wxid, file_path)
        return status == 0

    def send_message_card(
        self,
        wxid: str,
        title: str,
        abstract: str,
        url: str,
        image_path: Optional[str] = None,
    ) -> bool:
        """
        说明:
            发送消息卡片

        参数:
            * `wxid`: 对方wxid
            * `title`: 消息卡片标题
            * `abstract`: 消息卡片摘要
            * `url`: 文章链接
            * `image_path`: 消息卡片显示的图片绝对路径，不需要可以不指定

        返回:
            * `bool`: 发送是否成功
        """

        status = self.robot.CSendArticle(
            self.wechat_pid, wxid, title, abstract, url, image_path
        )
        return status == 0

    def send_contact_card(self, receiver: str, shared_wxid: str, nickname: str) -> bool:
        """
        说明:
            发送名片

        参数:
            * `wxid`: 对方wxid
            * `shared_id`: 被分享人wxid
            * `nickname`: 名片显示的昵称

        返回:
            * `bool`: 是否操作成功
        """

        status = self.robot.CSendCard(self.wechat_pid, receiver, shared_wxid, nickname)
        return status == 0

    def send_at_message(
        self,
        group_id: str,
        at_users: Union[list[str], str],
        message: str,
        auto_nickname: bool = True,
    ) -> bool:
        """
        说明:
            发送群@消息，艾特所有人可以将AtUsers设置为`notify@all`。
            无目标群管理权限请勿使用艾特所有人

        参数:
            * `group_id`: 群聊ID
            * `at_users`: 被艾特的人列表
            * `message`: 消息内容
            * `auto_nickname`: 是否自动填充被艾特人昵称,默认自动填充

        返回:
            * `bool`: 是否操作成功
        """
        if "@chatroom" not in group_id:
            return False

        status = self.robot.CSendAtText(
            self.wechat_pid, group_id, at_users, message, auto_nickname
        )
        return status == 0

    def get_self_info(self) -> dict:
        """
        说明:
            获取个人信息

        返回:
            * `dict`: 调用成功返回个人信息，否则返回空字典
        """
        self_info = self.robot.CGetSelfInfo(self.wechat_pid)
        return json.loads(self_info)

    def get_contacts(self) -> list:
        """
        说明:
            获取所有联系人列表

        返回:
            * `list`: 调用成功返回通讯录列表，调用失败返回空列表

        """

        try:
            friend_tuple = self.robot.CGetFriendList(self.wechat_pid)
            self.AddressBook = [dict(i) for i in list(friend_tuple)]
        except IndexError:
            self.AddressBook = []
        return self.AddressBook

    def get_friend_list(self, use_cache: bool = True) -> list:
        """
        说明:
            从通讯录列表中筛选出好友列表

        参数:
            * `use_cache`: 是否使用缓存，默认使用

        返回:
            * `list`: 好友列表

        """
        if self.AddressBook is None or not use_cache:
            self.get_contacts()
        friend_list = [
            item
            for item in self.AddressBook
            if (item["wxType"] == 3 and item["wxid"][0:3] != "gh_")
        ]
        return friend_list

    def get_group_list(self, use_cache: bool = True) -> list:
        """
        说明:
            从通讯录列表中筛选出群聊列表

        参数:
            * `use_cache`: 是否使用缓存，默认使用

        返回:
            * `list`: 群聊列表
        """
        if self.AddressBook is None or not use_cache:
            self.get_contacts()
        chatroom_list = [item for item in self.AddressBook if item["wxType"] == 2]
        return chatroom_list

    def get_public_account_list(self, use_cache: bool = True) -> list:
        """
        说明:
            从通讯录列表中筛选出公众号列表

        参数:
            * `use_cache`: 是否使用缓存，默认使用

        返回:
            * `list`: 公众号列表

        """
        if self.AddressBook is None or not use_cache:
            self.get_contacts()
        official_account_list = [
            item
            for item in self.AddressBook
            if (item["wxType"] == 3 and item["wxid"][0:3] == "gh_")
        ]
        return official_account_list

    def search_friend_by_remark(
        self, remark: str, use_cache: bool = True
    ) -> Optional[dict]:
        """
        说明:
            通过备注搜索联系人

        参数:
            * `remark`: 好友备注
            * `use_cache`: 是否使用缓存，默认使用

        返回:
            * `dict | None`: 搜索到返回联系人信息，否则返回None
        """
        if self.AddressBook is None or not use_cache:
            self.get_contacts()
        for item in self.AddressBook:
            if item["wxRemark"] == remark:
                return item
        return None

    def search_friend_by_wxnumber(
        self, wxnumber: str, use_cache: bool = True
    ) -> Optional[dict]:
        """
        说明:
            通过微信号搜索联系人(非微信id)

        参数:
            * `wxnumber`: 联系人微信号
            * `use_cache`: 是否使用缓存，默认使用

        返回:
            * `dict | None`: 搜索到返回联系人信息，否则返回None
        """
        if self.AddressBook is None or not use_cache:
            self.get_contacts()
        for item in self.AddressBook:
            if item["wxNumber"] == wxnumber:
                return item
        return None

    def search_friend_by_nickname(
        self, nickname: str, use_cache: bool = True
    ) -> Optional[dict]:
        """
        说明:
            通过昵称搜索联系人

        参数:
            * `nickname`: 联系人昵称
            * `use_cache`: 是否使用缓存，默认使用

        返回:
            * `dict | None`: 搜索到返回联系人信息，否则返回None
        """
        if self.AddressBook is None or not use_cache:
            self.get_contacts()
        for item in self.AddressBook:
            if item["wxNickName"] == nickname:
                return item
        return None

    def get_user_info(self, wxid: str) -> dict:
        """
        说明:
            通过wxid查询联系人信息

        参数:
            * `wxid`: 联系人wxid

        返回:
            * `dict`: 联系人信息

        """

        userinfo = self.robot.CGetWxUserInfo(self.wechat_pid, wxid)
        return json.loads(userinfo)

    def get_group_members(self, group_id: str) -> Optional[dict]:
        """
        说明:
            获取群成员信息

        参数:
            * `group_id`: 群聊id

        返回:
            * `dict | None`: 获取成功返回群成员信息，失败返回None

        """
        info = dict(self.robot.CGetChatRoomMembers(self.wechat_pid, group_id))
        if not info:
            return None
        members = info["members"].split("^G")
        data = self.get_user_info(group_id)
        data["members"] = []
        for member in members:
            member_info = self.get_user_info(member)
            data["members"].append(member_info)
        return data

    def check_friend_status(self, wxid: str) -> int:
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

        return self.robot.CCheckFriendStatus(self.wechat_pid, wxid)

    def start_receive_message(self, port: int = 0) -> bool:
        """
        启动接收消息Hook

        Parameters
        ----------
        port : int
            socket的监听端口号.如果要使用连接点回调，则将端口号设置为0.

        Returns
        -------
        int
            启动成功返回0,失败返回非0值.

        """

        status = self.robot.CStartReceiveMessage(self.wechat_pid, port)
        return status == 0

    def stop_receice_message(self) -> bool:
        """
        停止接收消息Hook

        Returns
        -------
        bool

        """

        status = self.robot.CStopReceiveMessage(self.wechat_pid)
        return status == 0

    def get_db_handles(self) -> dict:
        """
        说明:
            获取数据库句柄和表信息

        返回:
            * `dict`: 数据库句柄和表信息
        """

        tables_tuple = self.robot.CGetDbHandles(self.wechat_pid)
        tables = [dict(i) for i in tables_tuple]
        dbs = {}
        for table in tables:
            dbname = table["dbname"]
            if dbname not in dbs.keys():
                dbs[dbname] = {"Handle": table["Handle"], "tables": []}
            dbs[dbname]["tables"].append(
                {
                    "name": table["name"],
                    "tbl_name": table["tbl_name"],
                    "root_page": table["rootpage"],
                    "sql": table["sql"],
                }
            )
        return dbs

    def execute_sql(self, handle: int, sql: str) -> list:
        """
        说明:
            执行SQL

        参数:
            * `handle`: 数据库句柄
            * `sql`: SQL语句内容

        返回:
            * `list`: 查询结果

        """

        result = self.robot.CExecuteSQL(self.wechat_pid, handle, sql)
        if len(result) == 0:
            return []
        query_list = []
        keys = list(result[0])
        for item in result[1:]:
            query_dict = {}
            for key, value in zip(keys, item):
                query_dict[key] = (
                    value if not isinstance(value, tuple) else bytes(value)
                )
            query_list.append(query_dict)
        return query_list

    def backup_db(self, handle: int, file_path: str) -> bool:
        """
        说明:
            备份数据库

        参数:
            * `handle`: 数据库句柄
            * `file_path`: 备份文件保存位置

        返回:
            * `bool`: 操作是否成功

        """
        try:
            save_path = Path(file_path)
            save_path.parent.mkdir(parents=True, exist_ok=True)
            save_path = str(save_path.absolute())
        except Exception:
            return False
        status = self.robot.CBackupSQLiteDB(self.wechat_pid, handle, save_path)
        return status == 1

    def verify_friend_apply(self, v3: str, v4: str) -> bool:
        """
        说明:
            通过好友请求

        参数:
            * `v3`: v3数据(encryptUserName)
            * `v4`: v4数据(ticket)

        返回:
            * `bool`: 操作是否成功
        """

        status = self.robot.CVerifyFriendApply(self.wechat_pid, v3, v4)
        return status == 0

    def add_friend_by_wxid(self, wxid: str, message: Optional[str]) -> bool:
        """
        说明:
            发送好友请求（使用wxid）

        参数:
            * `wxid`: 要添加的wxid
            * `message`: 验证信息

        返回:
            * `bool`: 请求是否成功
        """

        status = self.robot.CAddFriendByWxid(self.wechat_pid, wxid, message)
        return status == 0

    def add_friend_by_v3(
        self,
        v3: str,
        message: Optional[str],
        add_type: Literal[0x1, 0x3, 0x6, 0xF] = 0x6,
    ) -> bool:
        """
        说明:
            发送好友请求（使用v3数据）

        参数:
            * `v3`: v3数据(encryptUserName)
            * `message`: 验证信息
            * `add_type`: 添加方式(来源)
                * `0x1`: QQ号
                * `0x3`: 微信号
                * `0x6`: 朋友验证消息
                * `0xF`: 手机号

        返回:
            * `bool`: 请求是否成功
        """

        status = self.robot.CAddFriendByV3(self.wechat_pid, v3, message, add_type)
        return status == 0

    def get_wechat_version(self) -> str:
        """
        说明:
            获取微信版本号

        返回:
            * `str`: 微信版本号

        """

        return self.robot.CGetWeChatVer()

    def search_user_info(self, keyword: str) -> Optional[dict]:
        """
        说明:
            网络查询用户信息

        参数:
            * `keyword`: 查询关键字，可以是微信号、手机号、QQ号

        返回:
            * `dict | None`: 查询成功返回用户信息,查询失败返回None
        """

        userinfo = self.robot.CSearchContactByNet(self.wechat_pid, keyword)
        if userinfo:
            return dict(userinfo)
        return None

    def follow_public_number(self, public_id: str) -> bool:
        """
        说明:
            关注公众号

        参数:
            * `public_id`: 公众号id

        返回:
            * `bool`: 操作是否成功

        """

        status = self.robot.CAddBrandContact(self.wechat_pid, public_id)
        return status == 0

    def change_wechat_version(self, version: str) -> bool:
        """
        说明:
            自定义微信版本号，一定程度上防止自动更新

        参数:
            * `version`: 版本号，类似`3.7.0.26`

        返回:
            * `bool`: 操作是否成功

        """

        status = self.robot.CChangeWeChatVer(self.wechat_pid, version)
        return status == 0

    def hook_image_msg(self, save_path: str) -> bool:
        """
        开始Hook未加密图片

        Parameters
        ----------
        save_path : str
            图片保存路径(绝对路径).

        Returns
        -------
        bool

        """

        status = self.robot.CHookImageMsg(self.wechat_pid, save_path)
        return status == 0

    def unhook_image_msg(self) -> bool:
        """
        取消Hook未加密图片

        Returns
        -------
        bool

        """

        status = self.robot.CUnHookImageMsg(self.wechat_pid)
        return status == 0

    def hook_voice_msg(self, save_path: str) -> bool:
        """
        开始Hook语音消息

        Parameters
        ----------
        save_path : str
            语音保存路径(绝对路径).

        Returns
        -------
        bool

        """

        status = self.robot.CHookVoiceMsg(self.wechat_pid, save_path)
        return status == 0

    def unhook_voice_msg(self) -> bool:
        """
        取消Hook语音消息

        Returns
        -------
        bool

        """

        status = self.robot.CUnHookVoiceMsg(self.wechat_pid)
        return status == 0

    def delete_friend(self, wxid: str) -> bool:
        """
        说明:
            删除好友

        参数:
            * `wxid`: 被删除好友wxid

        返回:
            * `bool`: 操作是否成功

        """

        stauts = self.robot.CDeleteUser(self.wechat_pid, wxid)
        return stauts == 0

    def edit_remark(self, wxid: str, remark: Optional[str]) -> bool:
        """
        说明:
            修改好友或群聊备注

        参数:
            * `wxid`: wxid或group_id
            * `remark`: 要修改的备注

        返回:
            * `bool`: 操作是否成功
        """

        status = self.robot.CEditRemark(self.wechat_pid, wxid, remark)
        return status == 0

    def set_group_name(self, group_id: str, name: str) -> bool:
        """
        说明:
            修改群名称.请确认具有相关权限再调用。

        参数:
            * `group_id`: 群聊id
            * `name`: 要修改为的群名称

        返回:
            * `bool`: 操作是否成功
        """

        status = self.robot.CSetChatRoomName(self.wechat_pid, group_id, name)
        return status == 0

    def set_group_announcement(
        self, group_id: str, announcement: Optional[str]
    ) -> bool:
        """
        说明:
            设置群公告.请确认具有相关权限再调用。

        参数:
            * `group_id`: 群聊id
            * `announcement`: 公告内容

        返回:
            * `bool`: 操作是否成功

        """

        status = self.robot.CSetChatRoomAnnouncement(
            self.wechat_pid, group_id, announcement
        )
        return status == 0

    def set_group_nickname(self, group_id: str, nickname: str) -> bool:
        """
        说明:
            设置群内个人昵称

        参数:
            * `group_id`: 群聊id
            * `announcement`: 要修改为的昵称

        返回:
            * `bool`: 操作是否成功
        """

        stauts = self.robot.CSetChatRoomSelfNickname(
            self.wechat_pid, group_id, nickname
        )
        return stauts == 0

    def get_groupmember_nickname(self, group_id: str, wxid: str) -> str:
        """
        说明:
            获取群成员昵称

        参数:
            * `group_id`: 群聊id
            * `wxid`: 群成员wxid

        返回:
            * `str`: 成功返回群成员昵称,失败返回空字符串
        """

        return self.robot.CGetChatRoomMemberNickname(self.wechat_pid, group_id, wxid)

    def delete_groupmember(self, group_id: str, wxid_list: Union[str, list]) -> bool:
        """
        说明:
            删除群成员.请确认具有相关权限再调用。

        参数:
            * `group_id`: 群聊id
            * `wxid_list`: 要删除的成员wxid或wxid列表

        返回:
            * `bool`: 操作是否成功
        """

        status = self.robot.CDelChatRoomMember(self.wechat_pid, group_id, wxid_list)
        return status == 0

    def add_groupmember(self, group_id: str, wxid_list: Union[str, list]) -> bool:
        """
        说明:
            添加群成员.请确认具有相关权限再调用。

        参数:
            * `group_id`: 群聊id
            * `wxid_list`: 要添加的成员wxid或wxid列表

        返回:
            * `bool`: 操作是否成功
        """

        status = self.robot.CAddChatRoomMember(self.wechat_pid, group_id, wxid_list)
        return status == 0

    def open_browser(self, url: str) -> bool:
        """
        说明:
            打开微信内置浏览器

        参数:
            * `url`: 目标网页url

        返回:
            * `bool`: 操作是否成功
        """

        status = self.robot.COpenBrowser(self.wechat_pid, url)
        return status == 0

    def get_history_public_msg(self, public_id: str, offset: str = "") -> dict:
        """
        说明:
            获取公众号历史消息，一次获取十条推送记录

        参数:
            * `public_id`: 公众号id
            * `offset`: 起始偏移，为空的话则从新到久获取十条，该值可从返回数据中取得. The default is ""

        返回:
            * `bool`: 操作是否成功
        """

        ret = self.robot.CGetHistoryPublicMsg(self.wechat_pid, public_id, offset)[0]
        try:
            ret = json.loads(ret)
        except json.JSONDecodeError:
            pass
        return ret

    def send_forward_msg(self, wxid: str, message_id: int) -> bool:
        """
        说明:
            转发消息，只支持单条转发

        参数:
            * `wxid`: 消息接收人wxid
            * `message_id`: 消息id，可以在实时消息接口中获取.

        返回:
            * `bool`: 操作是否成功
        """

        status = self.robot.CForwardMessage(self.wechat_pid, wxid, message_id)
        return status == 0

    def get_qrcode_image(self) -> bytes:
        """
        获取二维码，同时切换到扫码登录

        Returns
        -------
        bytes
            二维码bytes数据.
        You can convert it to image object,like this:
        >>> from io import BytesIO
        >>> from PIL import Image
        >>> buf = wx.GetQrcodeImage()
        >>> image = Image.open(BytesIO(buf)).convert("L")
        >>> image.save('./qrcode.png')

        """

        data = self.robot.CGetQrcodeImage(self.wechat_pid)
        return bytes(data)

    def get_a8key(self, url: str) -> Union[dict, str]:
        """
        说明:
            获取A8Key

        参数:
            * `url`: 公众号文章链接

        返回:
            * `dict | str`: 成功返回A8Key信息，失败返回空字符串
        """

        ret = self.robot.CGetA8Key(self.wechat_pid, url)
        try:
            ret = json.loads(ret)
        except json.JSONDecodeError:
            pass
        return ret

    def send_xml(self, wxid: str, xml: str, image_path: str = "") -> bool:
        """
        说明:
            发送原始xml消息

        参数:
            * `wxid`: 消息接收人
            * `xml`: xml内容
            * `image_path`: 图片路径. 默认为空.

        返回:
            * `bool`: 操作是否成功
        """

        status = self.robot.CSendXmlMsg(self.wechat_pid, wxid, xml, image_path)
        return status == 0

    def logout(self) -> bool:
        """
        退出登录

        Returns
        -------
        int
            成功返回0，失败返回非0值.

        """

        status = self.robot.CLogout(self.wechat_pid)
        return status == 0

    def get_transfer(self, wxid: str, transcationid: str, transferid: str) -> bool:
        """
        说明:
            收款

        参数:
            * `wxid`: 转账人wxid
            * `transcationid`: 从转账消息xml中获取
            * `transferid`: 从转账消息xml中获取

        返回:
            * `bool`: 操作是否成功
        """

        status = self.robot.CGetTransfer(
            self.wechat_pid, wxid, transcationid, transferid
        )
        return status == 0

    def send_gif(self, wxid: str, image_path: str) -> bool:
        """
        说明:
            发送gif表情

        参数:
            * `wxid`: 发送id
            * `image_path`: 图片路径

        返回:
            * `bool`: 操作是否成功
        """

        status = self.robot.CSendEmotion(self.wechat_pid, wxid, image_path)
        return status == 0

    def _GetMsgCDN(self, msgid: int) -> str:
        """
        下载图片、视频、文件

        Parameters
        ----------
        msgid : int
            msgid.

        Returns
        -------
        str
            成功返回文件路径，失败返回空字符串.

        """

        return self.robot.CGetMsgCDN(self.wechat_pid, msgid)

    async def get_msg_cdn(self, msgid: int) -> str:
        """
        下载图片、视频、文件

        Parameters
        ----------
        msgid : int
            msgid.

        Returns
        -------
        str
            成功返回文件路径，失败返回空字符串.

        """
        path = self._GetMsgCDN(msgid=msgid)
        if path != "":
            file = Path(path)
            while not file.exists():
                await asyncio.sleep(0.5)
        return path
