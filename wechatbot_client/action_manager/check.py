"""
用来检测action参数的模块
"""

from inspect import Parameter
from typing import Callable, ParamSpec, Type, TypeVar

from pydantic import BaseConfig, BaseModel, Extra, ValidationError, create_model

from wechatbot_client.consts import PREFIX
from wechatbot_client.utils import get_typed_signature, logger_wrapper

from .model import ActionRequest

ACTION_DICT: dict[str, Type[BaseModel]] = {}
"""标准action模型字典"""

P = ParamSpec("P")
R = TypeVar("R")
log = logger_wrapper("Action Manager")


class ModelConfig(BaseConfig):
    """action模型config"""

    extra = Extra.forbid


def check_action_params(request: ActionRequest) -> tuple[str, BaseModel]:
    """
    说明:
        检测action的参数合法性，会检测`action`是否存在，同时param类型是否符合

    参数:
        * `request`：action请求

    返回:
        * `str`: action的函数名
        * `BaseModel`: action的参数模型

    错误:
        * `TypeError`: 未实现action
        * `ValueError`: 参数错误
    """
    if request.params is None:
        request.params = {}

    action_model = ACTION_DICT.get(request.action)
    if action_model is None:
        log("ERROR", f"<r>未实现的action:{request.action}</r>")
        raise TypeError(f"未实现的action:{request.action}")

    try:
        model = action_model.parse_obj(request.params)
    except ValidationError as e:
        log("ERROR", f"<r>action参数错误:{e}</r>")
        raise ValueError("请求参数错误...")
    return action_model.__name__, model


def standard_action(func: Callable[P, R]) -> Callable[P, R]:
    """
    说明:
        使用此装饰器表示将此函数加入标准action字典中，会生成验证模型，注意参数的类型标注
    """

    global ACTION_DICT
    signature = get_typed_signature(func)
    field = {}
    for parameter in signature.parameters.values():
        name = parameter.name
        annotation = parameter.annotation
        default = parameter.default
        if name != "self":
            if default == Parameter.empty:
                field[name] = (annotation, ...)
            else:
                field[name] = (annotation, default)
    action_type = create_model(func.__name__, __config__=ModelConfig, **field)
    ACTION_DICT[func.__name__] = action_type
    return func


def expand_action(func: Callable[P, R]) -> Callable[P, R]:
    """
    说明:
        使用此装饰器表示将此函数加入拓展action字典中，会生成验证模型，注意参数的类型标注
        拓展action会使用<PREFIX>.action
    """

    global ACTION_DICT
    signature = get_typed_signature(func)
    field = {}
    for parameter in signature.parameters.values():
        name = parameter.name
        annotation = parameter.annotation
        default = parameter.default
        if name != "self":
            if default == Parameter.empty:
                field[name] = (annotation, ...)
            else:
                field[name] = (annotation, default)
    action_type = create_model(func.__name__, __config__=ModelConfig, **field)
    action_name = f"{PREFIX}.{func.__name__}"
    ACTION_DICT[action_name] = action_type
    return func


def get_supported_actions() -> list[str]:
    """
    获取支持的动作列表
    """
    return list(ACTION_DICT.keys())
