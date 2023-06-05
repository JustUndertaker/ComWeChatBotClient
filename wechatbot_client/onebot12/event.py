from typing import Literal

from pydantic import BaseModel, Extra

from wechatbot_client.consts import PLATFORM, PREFIX

from .message import Message


class BotSelf(BaseModel):
    """机器人自身"""

    platform: str = PLATFORM
    """消息平台"""
    user_id: str
    """机器人用户 ID"""


class BaseEvent(BaseModel, extra=Extra.allow):
    """
    基础事件
    """

    id: str
    """事件id"""
    time: float
    """时间"""
    type: Literal["message", "notice", "request", "meta"]
    """类型"""
    detail_type: str
    """细节类型"""
    sub_type: str = ""
    """子类型"""


class Event(BaseEvent, extra=Extra.allow):
    """OneBot V12 协议事件，字段与 OneBot 一致

    参考文档：[OneBot 文档](https://12.1bot.dev)
    """

    self: BotSelf
    """自身标识"""


class MessageEvent(Event):
    """
    消息事件
    """

    type: Literal["message"] = "message"
    """事件类型"""
    message_id: str
    """消息id"""
    message: Message
    """消息"""
    alt_message: str
    """消息替代表示"""
    user_id: str
    """用户id"""


class PrivateMessageEvent(MessageEvent):
    """私聊消息"""

    detail_type: Literal["private"] = "private"


class GroupMessageEvent(MessageEvent):
    """群消息"""

    detail_type: Literal["group"] = "group"
    group_id: str
    """群聊id"""


class NoticeEvent(Event):
    """通知事件"""

    type: Literal["notice"] = "notice"


class FriendIncreaseEvent(NoticeEvent):
    """好友增加事件"""

    detail_type: Literal["friend_increase"] = "friend_increase"
    user_id: str
    """添加id"""


# 无通知
class FriendDecreaseEvent(NoticeEvent):
    """好友减少事件"""

    detail_type: Literal["friend_decrease"] = "friend_decrease"
    user_id: str


class PrivateMessageDeleteEvent(NoticeEvent):
    """私聊消息删除"""

    detail_type: Literal["private_message_delete"] = "private_message_delete"
    message_id: str
    user_id: str


class GroupMemberIncreaseEvent(NoticeEvent):
    """群成员增加事件"""

    detail_type: Literal["group_member_increase"] = "group_member_increase"
    group_id: str
    """群id"""
    user_id: str
    """群成员id"""
    operator_id: str
    """操作者id"""


class GroupMemberDecreaseEvent(NoticeEvent):
    """群成员减少事件"""

    detail_type: Literal["group_member_decrease"] = "group_member_decrease"
    group_id: str
    """群id"""
    user_id: str
    """被踢id"""
    operator_id: str
    """操作者id"""


class GroupAdminSetEvent(NoticeEvent):
    """群管理员设置事件"""

    detail_type: Literal["group_admin_set"] = "group_admin_set"
    group_id: str
    """群id"""
    user_id: str
    """用户id"""
    operator_id: str
    """操作者id"""


class GroupAdminUnsetEvent(NoticeEvent):
    """群管理员取消设置事件"""

    detail_type: Literal["group_admin_unset"] = "group_admin_unset"
    group_id: str
    """群id"""
    user_id: str
    """用户id"""
    operator_id: str
    """操作者id"""


class GroupMessageDeleteEvent(NoticeEvent):
    """群消息删除事件"""

    detail_type: Literal["group_message_delete"] = "group_message_delete"
    sub_type: Literal["delete"] = "delete"
    group_id: str
    """群id"""
    message_id: str
    """消息id"""
    user_id: str
    """用户id"""
    operator_id: str
    """操作者id"""


class GetPrivateFileNotice(NoticeEvent):
    """
    私聊接收文件通知，在接收到文件时会发送通知（此时文件还未下载）
    """

    detail_type = f"{PREFIX}.get_private_file"

    file_name: str
    """文件名"""
    file_length: int
    """文件长度"""
    md5: str
    """文件md5"""
    user_id: str
    """发送方id"""


class GetGroupFileNotice(NoticeEvent):
    """
    群聊接收文件通知，在接收到文件时会发送通知（此时文件还未下载）
    """

    detail_type = f"{PREFIX}.get_group_file"

    file_name: str
    """文件名"""
    file_length: int
    """文件长度"""
    md5: str
    """文件md5"""
    user_id: str
    """发送方id"""
    group_id: str
    """群聊id"""


class GetPrivateRedBagNotice(NoticeEvent):
    """
    私聊获取红包提示
    """

    detail_type = f"{PREFIX}.get_private_redbag"
    user_id: str
    """发送方id"""


class GetGroupRedBagNotice(NoticeEvent):
    """
    群聊获取红包提示
    """

    detail_type = f"{PREFIX}.get_group_redbag"
    group_id: str
    """群id"""
    user_id: str
    """发送方"""


class GetPrivatePokeNotice(NoticeEvent):
    """
    私聊拍一拍
    """

    detail_type = f"{PREFIX}.get_private_poke"
    user_id: str
    """接收方id"""
    from_user_id: str
    """发送方id"""


class GetGroupPokeNotice(NoticeEvent):
    """
    群聊拍一拍
    """

    detail_type = f"{PREFIX}.get_group_poke"
    group_id: str
    """群id"""
    user_id: str
    """接收方id"""
    from_user_id: str
    """发送方id"""


class GetGroupAnnouncementNotice(NoticeEvent):
    """
    群公告
    """

    detail_type = f"{PREFIX}.get_group_announcement"
    group_id: str
    """群id"""
    user_id: str
    """操作者"""
    text: str
    """公告内容"""


class GetPrivateCardNotice(NoticeEvent):
    """
    私聊获取名片
    """

    detail_type = f"{PREFIX}.get_private_card"
    user_id: str
    """发送方id"""
    v3: str
    """名片v3信息"""
    v4: str
    """名片v4信息"""
    nickname: str
    """名片nickname"""
    head_url: str
    """头像url"""
    province: str
    """省"""
    city: str
    """市"""
    sex: str
    """性别"""


class GetGroupCardNotice(NoticeEvent):
    """群聊获取名片"""

    detail_type = f"{PREFIX}.get_group_card"
    group_id: str
    """群聊id"""
    user_id: str
    """发送方id"""
    v3: str
    """名片v3信息"""
    v4: str
    """名片v4信息"""
    nickname: str
    """名片nickname"""
    head_url: str
    """头像url"""
    province: str
    """省"""
    city: str
    """市"""
    sex: str
    """性别"""


class RequestEvent(Event):
    """请求事件"""

    type: Literal["request"] = "request"


class FriendRequestEvent(RequestEvent):
    """
    好友请求
    """

    detail_type: str = f"{PREFIX}.friend_request"
    user_id: str
    """添加id"""
    v3: str
    """v3信息"""
    v4: str
    """v4信息"""
    nickname: str
    """昵称"""
    content: str
    """附加的话"""
    country: str
    """国家"""
    province: str
    """省份"""
    city: str
    """城市"""


class MetaEvent(BaseEvent):
    """元事件"""

    type: Literal["meta"] = "meta"


class HeartbeatMetaEvent(MetaEvent):
    """心跳事件"""

    detail_type: Literal["heartbeat"] = "heartbeat"
    interval: int
    # status: Status


class ConnectEvent(MetaEvent):
    """连接事件"""

    detail_type: Literal["connect"] = "connect"
    version: dict[str, str]
    """版本"""


class BotStatus(BaseModel):
    self: BotSelf
    online: bool


class Status(BaseModel):
    good: bool
    bots: list[BotStatus]


class StatusUpdateEvent(MetaEvent):
    """状态更新事件"""

    detail_type: Literal["status_update"] = "status_update"
    status: Status
