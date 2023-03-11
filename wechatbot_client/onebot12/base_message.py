import abc
from copy import deepcopy
from dataclasses import asdict, dataclass, field
from typing import (
    Any,
    Dict,
    Generic,
    Iterable,
    List,
    Optional,
    Tuple,
    Type,
    TypeVar,
    Union,
    overload,
)

from pydantic import parse_obj_as

T = TypeVar("T")
TMS = TypeVar("TMS", bound="MessageSegment")
TM = TypeVar("TM", bound="Message")


@dataclass
class MessageSegment(abc.ABC, Generic[TM]):
    """消息段基类"""

    type: str
    """消息段类型"""
    data: Dict[str, Any] = field(default_factory=dict)
    """消息段数据"""

    @classmethod
    @abc.abstractmethod
    def get_message_class(cls) -> Type[TM]:
        """获取消息数组类型"""
        raise NotImplementedError

    @abc.abstractmethod
    def __str__(self) -> str:
        """该消息段所代表的 str，在命令匹配部分使用"""
        raise NotImplementedError

    def __len__(self) -> int:
        return len(str(self))

    def __ne__(self: T, other: T) -> bool:
        return not self == other

    def __add__(self: TMS, other: Union[str, TMS, Iterable[TMS]]) -> TM:
        return self.get_message_class()(self) + other

    def __radd__(self: TMS, other: Union[str, TMS, Iterable[TMS]]) -> TM:
        return self.get_message_class()(other) + self

    @classmethod
    def __get_validators__(cls):
        yield cls._validate

    @classmethod
    def _validate(cls, value):
        if isinstance(value, cls):
            return value
        if not isinstance(value, dict):
            raise ValueError(f"Expected dict for MessageSegment, got {type(value)}")
        if "type" not in value:
            raise ValueError(
                f"Expected dict with 'type' for MessageSegment, got {value}"
            )
        return cls(type=value["type"], data=value.get("data", {}))

    def get(self, key: str, default: Any = None):
        return asdict(self).get(key, default)

    def keys(self):
        return asdict(self).keys()

    def values(self):
        return asdict(self).values()

    def items(self):
        return asdict(self).items()

    def copy(self: T) -> T:
        return deepcopy(self)

    @abc.abstractmethod
    def is_text(self) -> bool:
        """当前消息段是否为纯文本"""
        raise NotImplementedError


class Message(List[TMS], abc.ABC):
    """消息数组

    参数:
        message: 消息内容
    """

    def __init__(
        self,
        message: Union[str, None, Iterable[TMS], TMS] = None,
    ):
        super().__init__()
        if message is None:
            return
        elif isinstance(message, str):
            self.extend(self._construct(message))
        elif isinstance(message, MessageSegment):
            self.append(message)
        elif isinstance(message, Iterable):
            self.extend(message)
        else:
            self.extend(self._construct(message))  # pragma: no cover

    @classmethod
    @abc.abstractmethod
    def get_segment_class(cls) -> Type[TMS]:
        """获取消息段类型"""
        raise NotImplementedError

    def __str__(self) -> str:
        return "".join(str(seg) for seg in self)

    @classmethod
    def __get_validators__(cls):
        yield cls._validate

    @classmethod
    def _validate(cls, value):
        if isinstance(value, cls):
            return value
        elif isinstance(value, Message):
            raise ValueError(f"Type {type(value)} can not be converted to {cls}")
        elif isinstance(value, str):
            pass
        elif isinstance(value, dict):
            value = parse_obj_as(cls.get_segment_class(), value)
        elif isinstance(value, Iterable):
            value = [parse_obj_as(cls.get_segment_class(), v) for v in value]
        else:
            raise ValueError(
                f"Expected str, dict or iterable for Message, got {type(value)}"
            )
        return cls(value)

    @staticmethod
    @abc.abstractmethod
    def _construct(msg: str) -> Iterable[TMS]:
        """构造消息数组"""
        raise NotImplementedError

    def __add__(self: TM, other: Union[str, TMS, Iterable[TMS]]) -> TM:
        result = self.copy()
        result += other
        return result

    def __radd__(self: TM, other: Union[str, TMS, Iterable[TMS]]) -> TM:
        result = self.__class__(other)
        return result + self

    def __iadd__(self: TM, other: Union[str, TMS, Iterable[TMS]]) -> TM:
        if isinstance(other, str):
            self.extend(self._construct(other))
        elif isinstance(other, MessageSegment):
            self.append(other)
        elif isinstance(other, Iterable):
            self.extend(other)
        else:
            raise TypeError(f"Unsupported type {type(other)!r}")
        return self

    @overload
    def __getitem__(self: TM, __args: str) -> TM:
        """
        参数:
            __args: 消息段类型

        返回:
            所有类型为 `__args` 的消息段
        """

    @overload
    def __getitem__(self, __args: Tuple[str, int]) -> TMS:
        """
        参数:
            __args: 消息段类型和索引

        返回:
            类型为 `__args[0]` 的消息段第 `__args[1]` 个
        """

    @overload
    def __getitem__(self: TM, __args: Tuple[str, slice]) -> TM:
        """
        参数:
            __args: 消息段类型和切片

        返回:
            类型为 `__args[0]` 的消息段切片 `__args[1]`
        """

    @overload
    def __getitem__(self, __args: int) -> TMS:
        """
        参数:
            __args: 索引

        返回:
            第 `__args` 个消息段
        """

    @overload
    def __getitem__(self: TM, __args: slice) -> TM:
        """
        参数:
            __args: 切片

        返回:
            消息切片 `__args`
        """

    def __getitem__(
        self: TM,
        args: Union[
            str,
            Tuple[str, int],
            Tuple[str, slice],
            int,
            slice,
        ],
    ) -> Union[TMS, TM]:
        arg1, arg2 = args if isinstance(args, tuple) else (args, None)
        if isinstance(arg1, int) and arg2 is None:
            return super().__getitem__(arg1)
        elif isinstance(arg1, slice) and arg2 is None:
            return self.__class__(super().__getitem__(arg1))
        elif isinstance(arg1, str) and arg2 is None:
            return self.__class__(seg for seg in self if seg.type == arg1)
        elif isinstance(arg1, str) and isinstance(arg2, int):
            return [seg for seg in self if seg.type == arg1][arg2]
        elif isinstance(arg1, str) and isinstance(arg2, slice):
            return self.__class__([seg for seg in self if seg.type == arg1][arg2])
        else:
            raise ValueError("Incorrect arguments to slice")  # pragma: no cover

    def index(self, value: Union[TMS, str], *args) -> int:
        if isinstance(value, str):
            first_segment = next((seg for seg in self if seg.type == value), None)
            if first_segment is None:
                raise ValueError(f"Segment with type {value} is not in message")
            return super().index(first_segment, *args)
        return super().index(value, *args)

    def get(self: TM, type_: str, count: Optional[int] = None) -> TM:
        if count is None:
            return self[type_]

        iterator, filtered = (
            seg for seg in self if seg.type == type_
        ), self.__class__()
        for _ in range(count):
            seg = next(iterator, None)
            if seg is None:
                break
            filtered.append(seg)
        return filtered

    def count(self, value: Union[TMS, str]) -> int:
        return len(self[value]) if isinstance(value, str) else super().count(value)

    def append(self: TM, obj: Union[str, TMS]) -> TM:
        """添加一个消息段到消息数组末尾。

        参数:
            obj: 要添加的消息段
        """
        if isinstance(obj, MessageSegment):
            super().append(obj)
        elif isinstance(obj, str):
            self.extend(self._construct(obj))
        else:
            raise ValueError(f"Unexpected type: {type(obj)} {obj}")  # pragma: no cover
        return self

    def extend(self: TM, obj: Union[TM, Iterable[TMS]]) -> TM:
        """拼接一个消息数组或多个消息段到消息数组末尾。

        参数:
            obj: 要添加的消息数组
        """
        for segment in obj:
            self.append(segment)
        return self

    def copy(self: TM) -> TM:
        return deepcopy(self)

    def extract_plain_text(self) -> str:
        """提取消息内纯文本消息"""

        return "".join(str(seg) for seg in self if seg.is_text())
