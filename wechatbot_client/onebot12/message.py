"""
onebot12消息实现，直接搬运adapter-onebot12
"""
from typing import Iterable, Type

from wechatbot_client.consts import PLATFORM
from wechatbot_client.typing import overrides

from .base_message import Message as BaseMessage
from .base_message import MessageSegment as BaseMessageSegment


class MessageSegment(BaseMessageSegment["Message"]):
    """OneBot v12 协议 MessageSegment 适配。具体方法参考协议消息段类型或源码。"""

    @classmethod
    @overrides(BaseMessageSegment)
    def get_message_class(cls) -> Type["Message"]:
        return Message

    @overrides(BaseMessageSegment)
    def __str__(self) -> str:
        if self.type == "text":
            return self.data.get("text", "")
        params = ",".join(
            [f"{k}={str(v)}" for k, v in self.data.items() if v is not None]
        )
        return f"[{self.type}:{params}]"

    @overrides(BaseMessageSegment)
    def is_text(self) -> bool:
        return self.type == "text" or self.type == "quote"

    @staticmethod
    def text(text: str) -> "MessageSegment":
        """文本消息"""
        return MessageSegment("text", {"text": text})

    @staticmethod
    def mention(user_id: str) -> "MessageSegment":
        """at消息"""
        return MessageSegment("mention", {"user_id": user_id})

    @staticmethod
    def mention_all() -> "MessageSegment":
        """全体at消息"""
        return MessageSegment("mention_all", {})

    @staticmethod
    def image(file_id: str, file_path: str) -> "MessageSegment":
        """图片消息"""
        return MessageSegment("image", {"file_path": file_path, "file_id": file_id})

    @staticmethod
    def voice(file_id: str, file_path: str) -> "MessageSegment":
        """语音消息"""
        return MessageSegment(
            "voice", {f"{PLATFORM}.file_path": file_path, "file_id": file_id}
        )

    @staticmethod
    def video(file_id: str, file_path: str) -> "MessageSegment":
        """视频消息"""
        return MessageSegment(
            "video", {f"{PLATFORM}.file_path": file_path, "file_id": file_id}
        )

    @staticmethod
    def file(file_id: str, file_path: str) -> "MessageSegment":
        """文件消息"""
        return MessageSegment(
            "file", {f"{PLATFORM}.file_path": file_path, "file_id": file_id}
        )

    @staticmethod
    def location(
        latitude: float,  # 维度
        longitude: float,  # 经度
        title: str,  # 标题
        content: str,  # 描述
    ) -> "MessageSegment":
        """位置消息"""
        return MessageSegment(
            "location",
            {
                "latitude": latitude,
                "longitude": longitude,
                "title": title,
                "content": content,
            },
        )

    @staticmethod
    def reply(
        message_id: str,
    ) -> "MessageSegment":
        """引用消息"""
        return MessageSegment("reply", {"message_id": message_id})

    @staticmethod
    def card(
        user_id: str,  # 联系人id
        head_url: str,  # 头像url
        nickname: str,  # 昵称
        province: str,  # 省
        city: str,  # 城市
        sex: int,  # 性别
    ) -> "MessageSegment":
        """名片消息"""
        return MessageSegment(
            f"{PLATFORM}.card",
            {
                "user_id": user_id,
                "head_url": head_url,
                "nickname": nickname,
                "province": province,
                "city": city,
                "sex": sex,
            },
        )

    @staticmethod
    def link(
        tittle: str, des: str, url: str, image: str  # 标题  # 描述  # 链接url  # 大图位置
    ) -> "MessageSegment":
        """链接消息"""
        return MessageSegment(
            f"{PLATFORM}.link",
            {"tittle": tittle, "des": des, "url": url, "image": image},
        )


class Message(BaseMessage[MessageSegment]):
    @classmethod
    @overrides(BaseMessage)
    def get_segment_class(cls) -> Type[MessageSegment]:
        return MessageSegment

    @staticmethod
    @overrides(BaseMessage)
    def _construct(msg: str) -> Iterable[MessageSegment]:
        yield MessageSegment.text(msg)

    @overrides(BaseMessage)
    def extract_plain_text(self) -> str:
        return "".join(seg.data["text"] for seg in self if seg.is_text())

    def ruduce(self) -> None:
        index = 1
        while index < len(self):
            if self[index - 1].type == "text" and self[index].type == "text":
                self[index - 1].data["text"] += self[index].data["text"]
                del self[index]
            else:
                index += 1
