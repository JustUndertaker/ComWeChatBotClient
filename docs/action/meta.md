# 元动作
:::tip Onebot12
元动作是用于对 OneBot 实现进行控制、检查等的动作，例如获取版本信息等，仅与 OneBot 本身交互，与实现对应的机器人平台无关。
:::

## 获取最新事件列表<Badge text="标准" type="success" />
action: `get_latest_events`

仅 HTTP 通信方式支持，用于轮询获取事件。
:::tabs

@tab 请求参数
| 字段名    | 数据类型 | 默认值   |    说明    |
| :-------: | :------: | :------: | :--------: |
| `limit` | int64 | 0 | 获取的事件数量上限，0 表示不限制 |
| `timeout` | int64 | 0 | 没有事件时最多等待的秒数，0 表示使用短轮询，不等待 |

@tab 响应数据
除元事件外的事件列表，从旧到新排序。

@tab 请求示例
```json
{
    "action": "get_latest_events",
    "params": {
        "limit": 100,
        "timeout": 0
    }
}
```

@tab 响应示例
```json
{
    "status": "ok",
    "retcode": 0,
    "data": [
        {
            "id": "b6e65187-5ac0-489c-b431-53078e9d2bbb",
            "self": {
                "platform": "wechat",
                "user_id": "123234"
            },
            "time": 1632847927.599013,
            "type": "message",
            "detail_type": "private",
            "sub_type": "",
            "message_id": "6283",
            "message": [
                {
                    "type": "text",
                    "data": {
                        "text": "OneBot is not a bot"
                    }
                },
                {
                    "type": "image",
                    "data": {
                        "file_id": "e30f9684-3d54-4f65-b2da-db291a477f16"
                    }
                }
            ],
            "alt_message": "OneBot is not a bot[图片]",
            "user_id": "123456788"
        },
        {
            "id": "b6e65187-5ac0-489c-b431-53078e9d2bbb",
            "self": {
                "platform": "qq",
                "user_id": "123234"
            },
            "time": 1632847927.599013,
            "type": "notice",
            "detail_type": "group_member_increase",
            "sub_type": "join",
            "user_id": "123456788",
            "group_id": "87654321",
            "operator_id": "1234567"
        }
    ],
    "message": ""
}
```

@tab 在nb2使用
```python
from nonebot.adapters.onebot.v12 import Bot
from nonebot import get_bot

async def test():
    bot = get_bot()
    latest_events = await bot.get_latest_events()

```
:::

## 获取支持的动作列表<Badge text="标准" type="success" />
action: `get_supported_actions`
:::tabs

@tab 请求参数
无.

@tab 响应数据
支持的动作名称列表，不包括 `get_latest_events`。

@tab 请求示例
```json
{
    "action": "get_supported_actions",
    "params": {}
}
```

@tab 响应示例
```json
{
    "status": "ok",
    "retcode": 0,
    "data": [
        "get_supported_actions",
        "get_status",
        "get_version",
        "send_message",
        "get_self_info",
        "get_user_info",
        "get_friend_list",
        "get_group_info",
        "get_group_list",
        "get_group_member_info",
        "get_group_member_list",
        "set_group_name",
        "upload_file",
        "get_file",
        "wx.get_public_account_list",
        "wx.follow_public_number",
        "wx.search_friend_by_remark",
        "wx.search_friend_by_wxnumber",
        "wx.search_friend_by_nickname",
        "wx.check_friend_status",
        "wx.get_db_handles",
        "wx.execute_sql",
        "wx.backup_db",
        "wx.verify_friend_apply",
        "wx.get_wechat_version",
        "wx.change_wechat_version",
        "wx.delete_friend",
        "wx.edit_remark",
        "wx.set_group_announcement",
        "wx.set_group_nickname",
        "wx.get_groupmember_nickname",
        "wx.kick_groupmember",
        "wx.invite_groupmember",
        "wx.get_history_public_msg",
        "wx.send_forward_msg",
        "wx.send_xml",
        "wx.send_card",
        "wx.clean_file_cache"
    ],
    "message": ""
}
```

@tab 在nb2使用
```python
from nonebot.adapters.onebot.v12 import Bot
from nonebot import get_bot

async def test():
    bot = get_bot()
    supported_actions = await bot.get_supported_actions()

```
:::

## 获取运行状态<Badge text="标准" type="success" />
action: `get_status`
:::tabs

@tab 请求参数
无

@tab 响应数据
| 字段名    | 数据类型 |    说明    |
| :-------: | :------: | :--------: |
| `good` | bool | 是否各项状态都符合预期，OneBot 实现各模块均正常 |
| `bots` | list[object] | 当前 OneBot Connect 连接上所有机器人账号的状态列表 |

其中，`bots` 的每一个元素具有下面这些字段：
| 字段名    | 数据类型 |    说明    |
| :-------: | :------: | :--------: |
| self | self | 机器人自身标识 |
| online | bool | 	机器人账号是否在线（可收发消息等） |

@tab 请求示例
```json
{
    "action": "get_status",
    "params": {}
}
```

@tab 响应示例
```json
{
    "status": "ok",
    "retcode": 0,
    "data": {
        "good": true,
        "bots": [
            {
                "self": {
                    "platform": "wechat",
                    "user_id": "xxxx"
                },
                "online": true
            }
        ]
    },
    "message": ""
}
```

@tab 在nb2使用
```python
from nonebot.adapters.onebot.v12 import Bot
from nonebot import get_bot

async def test():
    bot = get_bot()
    status = await bot.get_status()

```
:::

## 获取版本信息<Badge text="标准" type="success" />
action: `get_version`
:::tabs

@tab 请求参数
无

@tab 响应数据
| 字段名    | 数据类型 |    说明    |
| :-------: | :------: | :--------: |
| `impl` | string | 实现名称，`ComWechat` |
| `version` | string | 版本号 |
| `onebot_version` | string | OneBot 标准版本号 |

@tab 请求示例
```json
{
    "action": "get_version",
    "params": {}
}
```

@tab 响应示例
```json
{
    "status": "ok",
    "retcode": 0,
    "data": {
        "impl": "ComWechat",
        "version": "v1.0",
        "onebot_version": "12"
    },
    "message": ""
}
```

@tab 在nb2使用
```python
from nonebot.adapters.onebot.v12 import Bot
from nonebot import get_bot

async def test():
    bot = get_bot()
    version = await bot.get_version()

```
:::
