"""
这里将comwechat收到的message解析为event
"""
import re
from pathlib import Path
from typing import Callable, Generic, Optional, TypeVar
from urllib.parse import unquote
from uuid import uuid4
from xml.etree import ElementTree as ET

from wechatbot_client.file_manager import FileManager
from wechatbot_client.onebot12 import Message, MessageSegment
from wechatbot_client.onebot12.event import (
    BotSelf,
    Event,
    GroupMessageEvent,
    PrivateMessageEvent,
    RevokeMessageNotice,
)

from .model import Message as WechatMessage
from .type import WxType

E = TypeVar("E", bound=Event)

HANDLE_DICT: dict[int, Callable[[WechatMessage], E]] = {}
"""消息处理器字典"""
APP_HANDLERS: list[Callable[[WechatMessage], E]] = []
"""app消息处理函数列表"""
SYS_HANDLERS: list[Callable[[WechatMessage], Optional[E]]] = []
"""系统消息处理函数列表"""


def add_handler(_tpye: int) -> Callable[[WechatMessage], E]:
    """
    添加消息处理器
    """

    def _handle(func: Callable[[WechatMessage], E]) -> Callable[[WechatMessage], E]:
        global HANDLE_DICT
        HANDLE_DICT[_tpye] = func
        return func

    return _handle


def get_handler(_type: int) -> Callable[[WechatMessage], E]:
    """
    获取消息处理器
    """
    return HANDLE_DICT[_type]


def add_app_handler(func: Callable[[WechatMessage], E]) -> Callable[[WechatMessage], E]:
    """
    添加app_handler
    """
    global APP_HANDLERS
    APP_HANDLERS.append(func)
    return func


class MessageHandler(Generic[E]):
    """
    微信消息处理器
    """

    image_path: str
    """图片文件路径"""
    voice_path: str
    """语音文件路径"""
    video_path: str
    """视频文件路径"""
    file_manager: FileManager
    """文件处理器"""

    def _find_file(file_path: str) -> Optional[Path]:
        """
        找个图片
        """
        jpg = Path(f"{file_path}.jpg")
        if jpg.exists():
            return jpg
        png = Path(f"{file_path}.png")
        if png.exists():
            return png
        gif = Path(f"{file_path}.gif")
        if gif.exists():
            return gif
        return None

    @add_handler(WxType.TEXT_MSG)
    def handle_text(self, msg: WechatMessage) -> E:
        """
        处理文本
        """
        # 获取at
        raw_xml = msg.extrainfo
        xml_obj = ET.fromstring(raw_xml)
        at_xml = xml_obj.find("./atuserlist")
        event_id = str(uuid4())
        if at_xml is None:
            # 没有at
            # 获取message
            message = Message(MessageSegment.text(msg.message))
            # 判断群聊还是私聊
            if "@chatroom" in msg.sender:
                return GroupMessageEvent(
                    id=event_id,
                    time=msg.timestamp,
                    self=BotSelf(user_id=msg.self),
                    message_id=str(msg.msgid),
                    message=message,
                    alt_message=str(message),
                    user_id=msg.wxid,
                    group_id=msg.sender,
                )
            return PrivateMessageEvent(
                id=event_id,
                time=msg.timestamp,
                self=BotSelf(user_id=msg.self),
                message_id=str(msg.msgid),
                message=message,
                alt_message=str(message),
                user_id=msg.wxid,
            )

        # 获取at
        at_list = at_xml.text.split(",")
        if at_list[0] == "":
            # pc微信发消息at时，会多一个','
            at_list.pop(0)

        # 这里用正则分割文本，来制造消息段，可能会有bug
        regex = r"(@[^@\s]+\s)"
        msg_list = re.split(regex, msg.message)
        new_msg = Message()
        for index, one_msg in enumerate(msg_list):
            if re.search(regex, one_msg) is None:
                new_msg.append(MessageSegment.text(one_msg))
            else:
                try:
                    at_one = at_list.pop(0)
                except IndexError:
                    # 这里已经没有at目标了
                    text = "".join(msg_list[index:])
                    new_msg.append(MessageSegment.text(text))
                    break
                if at_one == "notify@all":
                    new_msg.append(MessageSegment.mention_all())
                else:
                    new_msg.append(MessageSegment.mention(at_one))
        return GroupMessageEvent(
            id=event_id,
            time=msg.timestamp,
            self=BotSelf(user_id=msg.self),
            message_id=str(msg.msgid),
            message=new_msg,
            alt_message=str(message),
            user_id=msg.wxid,
            group_id=msg.sender,
        )

    @add_handler(WxType.IMAGE_MSG)
    def handle_image(self, msg: WechatMessage) -> E:
        """
        处理图片
        """
        event_id = str(uuid4())
        file_name = Path(msg.filepath).stem
        # 找图片
        file_path = self.image_path + file_name
        file = self._find_file(file_path)
        if file is None:
            return None
        file_id = self.file_manager.cache_file_id_from_path(file, file.name)
        message = Message(MessageSegment.image(file_id=file_id))
        # 检测是否为群聊
        if "@chatroom" in msg.sender:
            return GroupMessageEvent(
                id=event_id,
                time=msg.timestamp,
                self=BotSelf(user_id=msg.self),
                message_id=str(msg.msgid),
                message=message,
                alt_message=str(message),
                user_id=msg.wxid,
                group_id=msg.sender,
            )
        return PrivateMessageEvent(
            id=event_id,
            time=msg.timestamp,
            self=BotSelf(user_id=msg.self),
            message_id=str(msg.msgid),
            message=message,
            alt_message=str(message),
            user_id=msg.wxid,
        )

    @add_handler(WxType.EMOJI_MSG)
    async def handle_emoji(self, msg: WechatMessage) -> E:
        """
        处理gif表情
        """
        event_id = str(uuid4())
        # 获取文件名
        raw_xml = msg.message
        xml_obj = ET.fromstring(raw_xml)
        emoji_url = xml_obj.find("./emoji").attrib.get("cdnurl")
        emoji = unquote(emoji_url)
        file_id = await self.file_manager.cache_file_id_from_url(
            emoji, f"{msg.msgid}.gif"
        )
        message = Message(MessageSegment.image(file_id=file_id))
        # 检测是否为群聊
        if "@chatroom" in msg.sender:
            return GroupMessageEvent(
                id=event_id,
                time=msg.timestamp,
                self=BotSelf(user_id=msg.self),
                message_id=str(msg.msgid),
                message=message,
                alt_message=str(message),
                user_id=msg.wxid,
                group_id=msg.sender,
            )
        return PrivateMessageEvent(
            id=event_id,
            time=msg.timestamp,
            self=BotSelf(user_id=msg.self),
            message_id=str(msg.msgid),
            message=message,
            alt_message=str(message),
            user_id=msg.wxid,
        )

    @add_handler(WxType.VOICE_MSG)
    def handle_voice(self, msg: WechatMessage) -> E:
        """
        处理语音
        """
        event_id = str(uuid4())
        file_name = msg.sign
        file = f"{self.voice_path}{file_name}.amr"
        file = Path(file)
        file_id = self.file_manager.cache_file_id_from_path(file, file.name)
        message = Message(MessageSegment.image(file_id=file_id))
        # 检测是否为群聊
        if "@chatroom" in msg.sender:
            return GroupMessageEvent(
                id=event_id,
                time=msg.timestamp,
                self=BotSelf(user_id=msg.self),
                message_id=str(msg.msgid),
                message=message,
                alt_message=str(message),
                user_id=msg.wxid,
                group_id=msg.sender,
            )
        return PrivateMessageEvent(
            id=event_id,
            time=msg.timestamp,
            self=BotSelf(user_id=msg.self),
            message_id=str(msg.msgid),
            message=message,
            alt_message=str(message),
            user_id=msg.wxid,
        )

    @add_handler(WxType.VIDEO_MSG)
    def handle_video(self, msg: WechatMessage) -> E:
        """
        处理视频
        """
        event_id = str(uuid4())
        video_img = Path(self.video_path + msg.thumb_path)
        video_name = video_img.stem
        return

    @add_handler(WxType.CARD_MSG)
    def handle_card(self, msg: WechatMessage) -> E:
        """
        处理名片消息
        """
        event_id = str(uuid4())
        raw_xml = msg.message
        xml_obj = ET.fromstring(raw_xml)
        attrib = xml_obj.attrib
        message = Message(
            MessageSegment.card(
                v3=attrib["username"],
                v4=attrib["antispamticket"],
                head_url=attrib["bigheadimgurl"],
                province=attrib["province"],
                city=attrib["city"],
                sex=attrib["sex"],
            )
        )
        # 检测是否为群聊
        if "@chatroom" in msg.sender:
            return GroupMessageEvent(
                id=event_id,
                time=msg.timestamp,
                self=BotSelf(user_id=msg.self),
                message_id=str(msg.msgid),
                message=message,
                alt_message=str(message),
                user_id=msg.wxid,
                group_id=msg.sender,
            )
        return PrivateMessageEvent(
            id=event_id,
            time=msg.timestamp,
            self=BotSelf(user_id=msg.self),
            message_id=str(msg.msgid),
            message=message,
            alt_message=str(message),
            user_id=msg.wxid,
        )

    @add_handler(WxType.LOCATION_MSG)
    def handle_location(self, msg: WechatMessage) -> E:
        """
        处理位置信息
        """
        event_id = str(uuid4())
        raw_xml = msg.message
        xml_obj = ET.fromstring(raw_xml)
        attrib = xml_obj.attrib
        message = Message(
            MessageSegment.location(
                latitude=attrib["x"],
                longitude=attrib["y"],
                title=attrib["label"],
                content=attrib["poiname"],
            )
        )
        # 检测是否为群聊
        if "@chatroom" in msg.sender:
            return GroupMessageEvent(
                id=event_id,
                time=msg.timestamp,
                self=BotSelf(user_id=msg.self),
                message_id=str(msg.msgid),
                message=message,
                alt_message=str(message),
                user_id=msg.wxid,
                group_id=msg.sender,
            )
        return PrivateMessageEvent(
            id=event_id,
            time=msg.timestamp,
            self=BotSelf(user_id=msg.self),
            message_id=str(msg.msgid),
            message=message,
            alt_message=str(message),
            user_id=msg.wxid,
        )

    @add_handler(WxType.REVOKE_NOTICE)
    def handle_revoke(self, msg: WechatMessage) -> E:
        """
        撤回消息事件
        """
        event_id = str(uuid4())
        raw_xml = msg.message
        xml_obj = ET.fromstring(raw_xml)
        message_id = xml_obj.find("./revokemsg/newmsgid").text
        return RevokeMessageNotice(
            id=event_id,
            time=msg.timestamp,
            self=BotSelf(user_id=msg.self),
            message_id=str(msg.msgid),
            group_id=msg.sender,
            user_id=msg.wxid,
            revoke_id=message_id,
        )
