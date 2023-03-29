# 个人动作

## 获取机器人自身信息<Badge text="标准" type="success" />
action: `get_self_info`

:::tabs

@tab 请求参数
无

@tab 响应数据
| 字段名    | 数据类型 |    说明    |
| :-------: | :------: | :--------: |
| `user_id` | string | 机器人用户 ID |
| `user_name` | string | 机器人昵称 |
| `user_displayname` | string | 为空 |

@tab 请求示例
```json
{
    "action": "get_self_info",
    "params": {}
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
        "user_displayname": ""
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
    self_info = await bot.get_self_info()

```

:::

## 获取用户信息<Badge text="标准" type="success" />
action: `get_user_info`

:::tabs

@tab 请求参数
| 字段名    | 数据类型 |    说明    |
| :-------: | :------: | :--------: |
| `user_id` | string | 用户 ID |

@tab 响应数据
| 字段名    | 数据类型 |    说明    |
| :-------: | :------: | :--------: |
| `user_id` | string | 用户 ID |
| `user_name` | string | 用户昵称 |
| `user_displayname` | string | 为空 |
| `user_remark` | string | 备注 |
| `wx.avatar` | string | `拓展字段:` 头像链接 |
| `wx.wx_number` | string | `拓展字段:` 微信号 |
| `wx.nation` | string | `拓展字段:` 国家 |
| `wx.province` | string | `拓展字段:` 省份 |
| `wx.city` | string | `拓展字段:` 城市 |

@tab 请求示例
```json
{
    "action": "get_user_info",
    "params": {
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
        "user_remark": "",
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
    user_info = await bot.get_user_info(user_id="1234567")
```
:::

## 获取好友列表<Badge text="标准" type="success" />
action: `get_friend_list`

:::tabs

@tab 请求参数
无

@tab 响应数据
好友信息列表，数据类型为 list[resp[`get_user_info`]]。

@tab 请求示例
```json
{
    "action": "get_friend_list",
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
            "user_id": "1234567",
            "user_name": "nb2",
            "user_displayname": "",
            "user_remark": "",
            "wx.verify_flag": "0"
        },
        {
            "user_id": "7654321",
            "user_name": "nb1",
            "user_displayname": "",
            "user_remark": "",
            "wx.verify_flag": "0",
        }
    ],
    "message": ""
}
```
`wx.verify_flag` 为好友验证标识。

@tab 在nb2使用
```python
from nonebot.adapters.onebot.v12 import Bot, MessageSegment
from nonebot import get_bot

async def test():
    bot = get_bot()
    friend_list = await bot.get_friend_list()

```

:::
