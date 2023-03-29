# 群组动作

## 获取群信息<Badge text="标准" type="success" />
action: `get_group_info`

:::tabs

@tab 请求参数
| 字段名    | 数据类型 |    说明    |
| :-------: | :------: | :--------: |
| `group_id` | string | 群 ID |

@tab 响应数据
| 字段名    | 数据类型 |    说明    |
| :-------: | :------: | :--------: |
| `group_id` | string | 群 ID |
| `group_name` | string | 群名称 |
| `wx.avatar` | string | `拓展字段:`群头像url |

@tab 请求示例
```json
{
    "action": "get_group_info",
    "params": {
        "group_id": "1234567"
    }
}
```

@tab 响应示例
```json
{
    "status": "ok",
    "retcode": 0,
    "data": {
        "group_id": "1234567",
        "group_name": "nb2",
        "wx.avatar": "https://wx.qlogo.cn/mmhead/ver_1/xxx/0"
    },
    "message": ""
}
```

@tab 在nb2使用
```python
from nonebot.adapters.onebot.v12 import Bot, MessageSegment
from nonebot import get_bot

async def test():
    bot = get_bot()
    group_info = await bot.get_group_info(group_id="1234567")

```

:::

## 获取群列表<Badge text="标准" type="success" />
action: `get_group_list`

:::tabs

@tab 请求参数
无

@tab 响应数据
群信息列表，数据类型为 list[resp[`get_group_info`]]。

@tab 请求示例
```json
{
    "action": "get_group_list",
    "params": {}
}
```

@tab 响应示例
```json
{
    "status": "ok",
    "retcode": 0,
    "data": [
        {
            "group_id": "1234567",
            "group_name": "nb2",
        },
        {
            "group_id": "1234568",
            "group_name": "nb2",
        }
    ],
    "message": ""
}
```

@tab 在nb2使用
```python
from nonebot.adapters.onebot.v12 import Bot, MessageSegment
from nonebot import get_bot

async def test():
    bot = get_bot()
    group_list = await bot.get_group_list()

```

:::

## 获取群成员信息<Badge text="标准" type="success" />
action: `get_group_member_info`

:::tabs

@tab 请求参数
| 字段名    | 数据类型 |    说明    |
| :-------: | :------: | :--------: |
| `group_id` | string | 群 ID |
| `user_id` | string | 用户 ID |

@tab 响应数据
| 字段名    | 数据类型 |    说明    |
| :-------: | :------: | :--------: |
| `user_id` | string | 用户 ID |
| `user_name` | string | 昵称 |
| `user_displayname` | string | 为空 |
| `wx.avatar` | string | `拓展字段:`头像url |
| `wx.wx_number` | string | `拓展字段:`微信号 |
| `wx.nation` | string | `拓展字段:`国家 |
| `wx.province` | string | `拓展字段:`省份 |
| `wx.city` | string | `拓展字段:`城市 |

@tab 请求示例
```json
{
    "action": "get_group_member_info",
    "params": {
        "group_id": "1234567",
        "user_id": "1234567"
    }
}
```

@tab 响应示例
```json
{
    "status": "ok",
    "retcode": 0,
    "data": {
        "user_id": "1234567",
        "user_name": "nb2",
        "user_displayname": "",
        "wx.avatar": "https://wx.qlogo.cn/mmhead/ver_1/xxx/0",
        "wx.wx_number": "nb2",
        "wx.nation": "中国",
        "wx.province": "广东",
        "wx.city": "深圳"
    },
    "message": ""
}
```

@tab 在nb2使用
```python
from nonebot.adapters.onebot.v12 import Bot, MessageSegment
from nonebot import get_bot

async def test():
    bot = get_bot()
    group_member_info = await bot.get_group_member_info(group_id="1234567", user_id="1234567")

```

:::

## 获取群成员列表<Badge text="标准" type="success" />
action: `get_group_member_list`

:::tabs

@tab 请求参数
| 字段名    | 数据类型 |    说明    |
| :-------: | :------: | :--------: |
| `group_id` | string | 群 ID |

@tab 响应数据
群成员信息列表，数据类型为 list[resp[`get_group_member_info`]]。

@tab 请求示例
```json
{
    "action": "get_group_member_list",
    "params": {
        "group_id": "1234567"
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
            "user_id": "1234567",
            "user_name": "nb2",
            "user_displayname": "",
            "wx.avatar": "https://wx.qlogo.cn/mmhead/ver_1/xxx/0",
            "wx.wx_number": "nb2",
            "wx.nation": "中国",
            "wx.province": "广东",
            "wx.city": "深圳"
        },
        {
            "user_id": "1234568",
            "user_name": "nb2",
            "user_displayname": "",
            "wx.avatar": "https://wx.qlogo.cn/mmhead/ver_1/xxx/0",
            "wx.wx_number": "nb2",
            "wx.nation": "中国",
            "wx.province": "广东",
            "wx.city": "深圳"
        }
    ],
    "message": ""
}
```

@tab 在nb2使用
```python
from nonebot.adapters.onebot.v12 import Bot, MessageSegment
from nonebot import get_bot

async def test():
    bot = get_bot()
    group_member_list = await bot.get_group_member_list(group_id="1234567")

```

:::

## 设置群名称<Badge text="标准" type="success" />
action: `set_group_name`

:::tabs

@tab 请求参数
| 字段名    | 数据类型 |    说明    |
| :-------: | :------: | :--------: |
| `group_id` | string | 群 ID |
| `group_name` | string | 群名称 |

@tab 响应数据
无

@tab 请求示例
```json
{
    "action": "set_group_name",
    "params": {
        "group_id": "1234567",
        "group_name": "nb2"
    }
}
```

@tab 响应示例
```json
{
    "status": "ok",
    "retcode": 0,
    "data": null,
    "message": ""
}
```

@tab 在nb2使用
```python
from nonebot.adapters.onebot.v12 import Bot, MessageSegment
from nonebot import get_bot

async def test():
    bot = get_bot()
    await bot.set_group_name(group_id="1234567", group_name="nb2")

```

:::

## 退出群<Badge text="标准" type="success" />
action: `leave_group`

:::danger Wechat
未实现
:::
