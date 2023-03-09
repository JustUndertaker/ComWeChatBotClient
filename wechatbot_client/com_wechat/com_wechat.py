import asyncio
import json
from pathlib import Path
from typing import Optional, Tuple, Union

import psutil
from comtypes.client import CreateObject, GetEvents, PumpEvents

from wechatbot_client.log import logger
from wechatbot_client.utils import escape_tag


class MessageReporter:
    """
    消息接收器
    """

    def OnGetMessageEvent(self, message: Tuple[str, None]):
        msg = message[0]
        logger.success(f"<g>接收到wechat消息</g> - {escape_tag(msg)}")


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

    async def _pump_event(self) -> None:
        """接收event"""
        while True:
            try:
                await asyncio.sleep(0)
                PumpEvents(0.01)
            except KeyboardInterrupt:
                logger.info("<g>事件接收已关闭，再使用 'ctrl + c' 结束进程...</g>")
                return

    def start_msg_recv(self) -> None:
        """
        开始接收消息
        """
        asyncio.create_task(self._pump_event())


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
            微信pid，为0则失败
        """
        return self.robot.CStartWeChat()

    def start_service(self) -> bool:
        """
        注入DLL到微信以启动服务

        Returns
        -------
        int
            0成功,非0失败.

        """
        status = self.robot.CStartRobotService(self.wechat_pid)
        return status == 0

    def stop_service(self) -> int:
        """
        停止服务，会将DLL从微信进程中卸载

        Returns
        -------
        int
            COM进程pid.

        """

        com_pid = self.robot.CStopRobotService(self.wechat_pid)
        return com_pid

    def is_wechat_login(self) -> bool:
        """
        获取微信登录状态

        Returns
        -------
        bool
            微信登录状态.

        """

        status = self.robot.CIsWxLogin(self.wechat_pid)
        return status == 1

    def send_text(self, receiver: str, msg: str) -> bool:
        """
        发送文本消息

        Parameters
        ----------
        receiver : str
            消息接收者wxid.
        msg : str
            消息内容.

        Returns
        -------
        int
            0成功,非0失败.

        """

        status = self.robot.CSendText(self.wechat_pid, receiver, msg)
        return status == 0

    def send_image(self, receiver: str, img_path: str) -> bool:
        """
        发送图片消息

        Parameters
        ----------
        receiver : str
            消息接收者wxid.
        img_path : str
            图片绝对路径.

        Returns
        -------
        int
            0成功,非0失败.

        """

        status = self.robot.CSendImage(self.wechat_pid, receiver, img_path)
        return status == 0

    def send_file(self, receiver: str, filepath: str) -> bool:
        """
        发送文件

        Parameters
        ----------
        receiver : str
            消息接收者wxid.
        filepath : str
            文件绝对路径.

        Returns
        -------
        int
            0成功,非0失败.

        """

        status = self.robot.CSendFile(self.wechat_pid, receiver, filepath)
        return status == 0

    def send_xml(
        self,
        receiver: str,
        title: str,
        abstract: str,
        url: str,
        img_path: Optional[str] = None,
    ) -> bool:
        """
        发送XML文章

        Parameters
        ----------
        receiver : str
            消息接收者wxid.
        title : str
            消息卡片标题.
        abstract : str
            消息卡片摘要.
        url : str
            文章链接.
        img_path : str or None, optional
            消息卡片显示的图片绝对路径，不需要可以不指定. The default is None.

        Returns
        -------
        int
            0成功,非0失败.

        """

        status = self.robot.CSendArticle(
            self.wechat_pid, receiver, title, abstract, url, img_path
        )
        return status == 0

    def send_card(self, receiver: str, shared_wxid: str, nickname: str) -> bool:
        """
        发送名片

        Parameters
        ----------
        receiver : str
            消息接收者wxid.
        shared_wxid : str
            被分享人wxid.
        nickname : str
            名片显示的昵称.

        Returns
        -------
        int
            0成功,非0失败.

        """

        status = self.robot.CSendCard(self.wechat_pid, receiver, shared_wxid, nickname)
        return status == 0

    def send_at_msg(
        self,
        chatroom_id: str,
        at_users: list or str or tuple,
        msg: str,
        auto_nickname: bool = True,
    ) -> bool:
        """
        发送群艾特消息，艾特所有人可以将AtUsers设置为`notify@all`
        无目标群管理权限请勿使用艾特所有人
        Parameters
        ----------
        chatroom_id : str
            群聊ID.
        at_users : list or str or tuple
            被艾特的人列表.
        msg : str
            消息内容.
        auto_nickname : bool, optional
            是否自动填充被艾特人昵称. 默认自动填充.

        Returns
        -------
        int
            0成功,非0失败.

        """
        if "@chatroom" not in chatroom_id:
            return False

        status = self.robot.CSendAtText(
            self.wechat_pid, chatroom_id, at_users, msg, auto_nickname
        )
        return status == 0

    def get_self_info(self) -> dict:
        """
        获取个人信息

        Returns
        -------
        dict
            调用成功返回个人信息，否则返回空字典.

        """
        self_info = self.robot.CGetSelfInfo(self.wechat_pid)
        return json.loads(self_info)

    def get_contacts(self) -> list:
        """
        获取联系人列表

        Returns
        -------
        list
            调用成功返回通讯录列表，调用失败返回空列表.

        """

        try:
            friend_tuple = self.robot.CGetFriendList(self.wechat_pid)
            self.AddressBook = [dict(i) for i in list(friend_tuple)]
        except IndexError:
            self.AddressBook = []
        return self.AddressBook

    def get_friend_list(self) -> list:
        """
        从通讯录列表中筛选出好友列表

        Returns
        -------
        list
            好友列表.

        """
        if not self.AddressBook:
            self.get_contacts()
        friend_list = [
            item
            for item in self.AddressBook
            if (item["wxType"] == 3 and item["wxid"][0:3] != "gh_")
        ]
        return friend_list

    def get_chatroom_list(self) -> list:
        """
        从通讯录列表中筛选出群聊列表

        Returns
        -------
        list
            群聊列表.

        """
        if not self.AddressBook:
            self.get_contacts()
        chatroom_list = [item for item in self.AddressBook if item["wxType"] == 2]
        return chatroom_list

    def get_official_account_list(self) -> list:
        """
        从通讯录列表中筛选出公众号列表

        Returns
        -------
        list
            公众号列表.

        """
        if not self.AddressBook:
            self.get_contacts()
        official_account_list = [
            item
            for item in self.AddressBook
            if (item["wxType"] == 3 and item["wxid"][0:3] == "gh_")
        ]
        return official_account_list

    def get_friend_by_remark(self, remark: str) -> Optional[dict]:
        """
        通过备注搜索联系人

        Parameters
        ----------
        remark : str
            好友备注.

        Returns
        -------
        dict or None
            搜索到返回联系人信息，否则返回None.

        """
        if not self.AddressBook:
            self.get_contacts()
        for item in self.AddressBook:
            if item["wxRemark"] == remark:
                return item
        return None

    def get_friend_by_wxid(self, wx_number: str) -> Optional[dict]:
        """
        通过微信号搜索联系人

        Parameters
        ----------
        wx_number : str
            联系人微信号.

        Returns
        -------
        dict or None
            搜索到返回联系人信息，否则返回None.

        """
        if not self.AddressBook:
            self.get_contacts()
        for item in self.AddressBook:
            if item["wxNumber"] == wx_number:
                return item
        return None

    def get_friend_by_nickname(self, nickname: str) -> Optional[dict]:
        """
        通过昵称搜索联系人

        Parameters
        ----------
        nickname : str
            联系人昵称.

        Returns
        -------
        dict or None
            搜索到返回联系人信息，否则返回None.

        """
        if not self.AddressBook:
            self.get_contacts()
        for item in self.AddressBook:
            if item["wxNickName"] == nickname:
                return item
        return None

    def get_user_info(self, wxid: str) -> dict:
        """
        通过wxid查询联系人信息

        Parameters
        ----------
        wxid : str
            联系人wxid.

        Returns
        -------
        dict
            联系人信息.

        """

        userinfo = self.robot.CGetWxUserInfo(self.wechat_pid, wxid)
        return json.loads(userinfo)

    def get_group_members(self, chatroom_id: str) -> Optional[dict]:
        """
        获取群成员信息

        Parameters
        ----------
        chatroom_id : str
            群聊id.

        Returns
        -------
        dict or None
            获取成功返回群成员信息，失败返回None.

        """
        info = dict(self.robot.CGetChatRoomMembers(self.wechat_pid, chatroom_id))
        if not info:
            return None
        members = info["members"].split("^G")
        data = self.GetWxUserInfo(chatroom_id)
        data["members"] = []
        for member in members:
            member_info = self.GetWxUserInfo(member)
            data["members"].append(member_info)
        return data

    def check_friend_status(self, wxid: str) -> int:
        """
        获取好友状态码

        Parameters
        ----------
        wxid : str
            好友wxid.

        Returns
        -------
        int
            0x0: 'Unknown',
            0xB0:'被删除',
            0xB1:'是好友',
            0xB2:'已拉黑',
            0xB5:'被拉黑',

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
        获取数据库句柄和表信息

        Returns
        -------
        dict
            数据库句柄和表信息.

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
        执行SQL

        Parameters
        ----------
        handle : int
            数据库句柄.
        sql : str
            SQL.

        Returns
        -------
        list
            查询结果.

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

    def backup_db(self, handle: int, filepath: str) -> bool:
        """
        备份数据库

        Parameters
        ----------
        handle : int
            数据库句柄.
        filepath : int
            备份文件保存位置.

        Returns
        -------
        bool

        """

        save_path = Path(filepath)
        save_path.mkdir(parents=True, exist_ok=True)
        status = self.robot.CBackupSQLiteDB(self.wechat_pid, handle, filepath)
        return status == 0

    def verify_friend_apply(self, v3: str, v4: str) -> bool:
        """
        通过好友请求

        Parameters
        ----------
        v3 : str
            v3数据(encryptUserName).
        v4 : str
            v4数据(ticket).

        Returns
        -------
        bool.

        """

        status = self.robot.CVerifyFriendApply(self.wechat_pid, v3, v4)
        return status == 0

    def add_friend_by_wxid(self, wxid: str, message: Optional[str]) -> bool:
        """
        wxid加好友

        Parameters
        ----------
        wxid : str
            要添加的wxid.
        message : str or None
            验证信息.

        Returns
        -------
        int
            请求发送成功返回0,失败返回非0值.

        """

        status = self.robot.CAddFriendByWxid(self.wechat_pid, wxid, message)
        return status == 0

    def add_friend_by_v3(
        self, v3: str, message: str or None, add_type: int = 0x6
    ) -> bool:
        """
        v3数据加好友

        Parameters
        ----------
        v3 : str
            v3数据(encryptUserName).
        message : str or None
            验证信息.
        add_type : int
            添加方式(来源).手机号: 0xF;微信号: 0x3;QQ号: 0x1;朋友验证消息: 0x6.

        Returns
        -------
        int
            请求发送成功返回0,失败返回非0值.

        """

        status = self.robot.CAddFriendByV3(self.wechat_pid, v3, message, add_type)
        return status == 0

    def get_wechat_version(self) -> str:
        """
        获取微信版本号

        Returns
        -------
        str
            微信版本号.

        """

        return self.robot.CGetWeChatVer()

    def search_user_info(self, keyword: str) -> Optional[dict]:
        """
        网络查询用户信息

        Parameters
        ----------
        keyword : str
            查询关键字，可以是微信号、手机号、QQ号.

        Returns
        -------
        dict or None
            查询成功返回用户信息,查询失败返回None.

        """

        userinfo = self.robot.CSearchContactByNet(self.wechat_pid, keyword)
        if userinfo:
            return dict(userinfo)
        return None

    def follow_public_number(self, public_id: str) -> bool:
        """
        关注公众号

        Parameters
        ----------
        public_id : str
            公众号id.

        Returns
        -------
        int
            请求成功返回0,失败返回非0值.

        """

        status = self.robot.CAddBrandContact(self.wechat_pid, public_id)
        return status == 0

    def change_wechat_version(self, version: str) -> bool:
        """
        自定义微信版本号，一定程度上防止自动更新

        Parameters
        ----------
        version : str
            版本号，类似`3.7.0.26`

        Returns
        -------
        bool

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

    def delete_user(self, wxid: str) -> bool:
        """
        删除好友

        Parameters
        ----------
        wxid : str
            被删除好友wxid.

        Returns
        -------
        bool

        """

        stauts = self.robot.CDeleteUser(self.wechat_pid, wxid)
        return stauts == 0

    def send_app_msg(self, wxid: str, appid: str) -> bool:
        """
        发送小程序

        Parameters
        ----------
        wxid : str
            消息接收者wxid.
        appid : str
            小程序id (在xml中是username，不是appid).

        Returns
        -------
        bool

        """

        status = self.robot.CSendAppMsg(self.wechat_pid, wxid, appid)
        return status == 0

    def edit_remark(self, wxid: str, remark: Optional[str]) -> bool:
        """
        修改好友或群聊备注

        Parameters
        ----------
        wxid : str
            wxid或chatroom_id.
        remark : str or None
            要修改的备注.

        Returns
        -------
        bool

        """

        status = self.robot.CEditRemark(self.wechat_pid, wxid, remark)
        return status == 0

    def set_group_name(self, chatroom_id: str, name: str) -> bool:
        """
        修改群名称.请确认具有相关权限再调用。

        Parameters
        ----------
        chatroom_id : str
            群聊id.
        name : str
            要修改为的群名称.

        Returns
        -------
        bool

        """

        status = self.robot.CSetChatRoomName(self.wechat_pid, chatroom_id, name)
        return status == 0

    def set_group_announcement(
        self, chatroom_id: str, announcement: Optional[str]
    ) -> bool:
        """
        设置群公告.请确认具有相关权限再调用。

        Parameters
        ----------
        chatroom_id : str
            群聊id.
        announcement : str or None
            公告内容.

        Returns
        -------
        bool

        """

        status = self.robot.CSetChatRoomAnnouncement(
            self.wechat_pid, chatroom_id, announcement
        )
        return status == 0

    def set_group_nickname(self, chatroom_id: str, nickname: str) -> bool:
        """
        设置群内个人昵称

        Parameters
        ----------
        chatroom_id : str
            群聊id.
        nickname : str
            要修改为的昵称.

        Returns
        -------
        bool

        """

        stauts = self.robot.CSetChatRoomSelfNickname(
            self.wechat_pid, chatroom_id, nickname
        )
        return stauts == 0

    def get_groupmember_nickname(self, chatroom_id: str, wxid: str) -> str:
        """
        获取群成员昵称

        Parameters
        ----------
        chatroom_id : str
            群聊id.
        wxid : str
            群成员wxid.

        Returns
        -------
        str
            成功返回群成员昵称,失败返回空字符串.

        """

        return self.robot.CGetChatRoomMemberNickname(self.wechat_pid, chatroom_id, wxid)

    def delete_groupmember(
        self, chatroom_id: str, wxid_list: Union[str, list, tuple]
    ) -> bool:
        """
        删除群成员.请确认具有相关权限再调用。

        Parameters
        ----------
        chatroom_id : str
            群聊id.
        wxid_list : str or list or tuple
            要删除的成员wxid或wxid列表.

        Returns
        -------
        bool

        """

        status = self.robot.CDelChatRoomMember(self.wechat_pid, chatroom_id, wxid_list)
        return status == 0

    def add_groupmember(
        self, chatroom_id: str, wxid_list: Union[str, list, tuple]
    ) -> bool:
        """
        添加群成员.请确认具有相关权限再调用。

        Parameters
        ----------
        chatroom_id : str
            群聊id.
        wxid_list : str or list or tuple
            要添加的成员wxid或wxid列表.

        Returns
        -------
        bool

        """

        status = self.robot.CAddChatRoomMember(self.wechat_pid, chatroom_id, wxid_list)
        return status == 0

    def open_browser(self, url: str) -> bool:
        """
        打开微信内置浏览器

        Parameters
        ----------
        url : str
            目标网页url.

        Returns
        -------
        bool

        """

        status = self.robot.COpenBrowser(self.wechat_pid, url)
        return status == 0

    def get_history_public_msg(self, public_id: str, offset: str = "") -> str:
        """
        获取公众号历史消息，一次获取十条推送记录

        Parameters
        ----------
        public_id : str
            公众号id.
        offset : str, optional
            起始偏移，为空的话则从新到久获取十条，该值可从返回数据中取得. The default is "".

        Returns
        -------
        str
            成功返回json数据，失败返回错误信息或空字符串.

        """

        ret = self.robot.CGetHistoryPublicMsg(self.wechat_pid, public_id, offset)[0]
        try:
            ret = json.loads(ret)
        except json.JSONDecodeError:
            pass
        return ret

    def forward_msg(self, wxid: str, msgid: int) -> bool:
        """
        转发消息，只支持单条转发

        Parameters
        ----------
        wxid : str
            消息接收人wxid.
        msgid : int
            消息id，可以在实时消息接口中获取.

        Returns
        -------
        int
            成功返回0，失败返回非0值.

        """

        status = self.robot.CForwardMessage(self.wechat_pid, wxid, msgid)
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
        获取A8Key

        Parameters
        ----------
        url : str
            公众号文章链接.

        Returns
        -------
        dict
            成功返回A8Key信息，失败返回空字符串.

        """

        ret = self.robot.CGetA8Key(self.wechat_pid, url)
        try:
            ret = json.loads(ret)
        except json.JSONDecodeError:
            pass
        return ret

    def send_origin_xml(self, wxid: str, xml: str, img_path: str = "") -> bool:
        """
        发送原始xml消息

        Parameters
        ----------
        wxid : str
            消息接收人.
        xml : str
            xml内容.
        img_path : str, optional
            图片路径. 默认为空.

        Returns
        -------
        int
            发送成功返回0，发送失败返回非0值.

        """

        status = self.robot.CSendXmlMsg(self.wechat_pid, wxid, xml, img_path)
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
        收款

        Parameters
        ----------
        wxid : str
            转账人wxid.
        transcationid : str
            从转账消息xml中获取.
        transferid : str
            从转账消息xml中获取.

        Returns
        -------
        int
            成功返回0，失败返回非0值.

        """

        status = self.robot.CGetTransfer(
            self.wechat_pid, wxid, transcationid, transferid
        )
        return status == 0

    def send_gif_msg(self, wxid: str, img_path: str) -> bool:
        """
        发送gif表情

        Parameters
        ----------
        wxid : str
            消息接收者wxid.
        img_path : str
            图片绝对路径.

        Returns
        -------
        int
            0成功,非0失败.

        """

        status = self.robot.CSendEmotion(self.wechat_pid, wxid, img_path)
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
