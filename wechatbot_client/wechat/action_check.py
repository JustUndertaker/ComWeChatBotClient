from inspect import Parameter
from typing import Type

from pydantic import BaseConfig, BaseModel, Extra, create_model

from wechatbot_client.com_wechat import ComWechatApi

from .utils import get_typed_signature

ACTION_LIST = [
    "send_text",
    "send_image",
    "send_file",
    "send_xml",
    "send_card",
    "send_at_msg",
    "get_self_info",
    "get_contacts",
    "get_friend_list",
    "get_chatroom_list",
    "get_official_account_list",
    "get_friend_by_remark",
    "get_friend_by_wxid",
    "get_friend_by_nickname",
    "get_user_info",
    "get_group_members",
    "check_friend_status",
    "start_receive_message",
    "stop_receice_message",
    "get_db_handles",
    "execute_sql",
    "backup_db",
    "verify_friend_apply",
    "add_friend_by_wxid",
    "add_friend_by_v3",
    "get_wechat_version",
    "search_user_info",
    "follow_public_number",
    "change_wechat_version",
    "delete_user",
    "send_app_msg",
    "edit_remark",
    "set_group_name",
    "set_group_announcement",
    "set_group_nickname",
    "get_groupmember_nickname",
    "delete_groupmember",
    "add_groupmember",
    "open_browser",
    "get_history_public_msg",
    "forward_msg",
    "get_qrcode_image",
    "get_a8key",
    "send_origin_xml",
    "logout",
    "get_transfer",
    "send_gif_msg",
    "get_msg_cdn",
]
"""action列表"""

ACTION_DICT: dict[str, Type[BaseModel]] = {}
"""action模型字典"""


class ModelConfig(BaseConfig):
    """action模型config"""

    extra = Extra.forbid


def gen_action_dict():
    """
    生成action字典
    """
    global ACTION_DICT
    field = {}
    for action in ACTION_LIST:
        call = getattr(ComWechatApi, action)
        signature = get_typed_signature(call)
        field.clear()
        for parameter in signature.parameters.values():
            name = parameter.name
            annotation = parameter.annotation
            default = parameter.default
            if name != "self":
                if default == Parameter.empty:
                    field[name] = (annotation, ...)
                else:
                    field[name] = (annotation, default)
        action_type = create_model(action, __config__=ModelConfig, **field)
        ACTION_DICT[action] = action_type
