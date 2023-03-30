# 消息动作


## 发送消息<Badge text="标准" type="success" />
action: `send_message`

:::warning Wechat
由于 wechat 的特性，该接口有以下限制:
 - `message_type` 只能为 `private` 或 `group`
 - `message` 中的每个消息段都将作为一条消息发送出去(除了`mention`)
 - `mention` 和 `mention_all` 只支持群聊
:::

:::tabs

@tab 请求参数
| 字段名    | 数据类型 |    说明    |
| :-------: | :------: | :--------: |
| `message_type` | string | 消息类型，`private` 或 `group` |
| `user_id` | string | 用户 ID，当 `detail_type` 为 `private` 时必须传入 |
| `group_id` | string | 群 ID，当 `detail_type` 为 `group` 时必须传入 |
| `message` | message | 消息内容，为消息段列表，详见 [消息段](/message/README.md) |

@tab 响应数据
在 `Onebot12` 标准中，原则上应该返回一个 `message_id`，但是由于hook的限制，目前只能返回一个 `bool`，用来判断消息是否发送成功。

@tab 请求示例
```json
{
    "action": "send_message",
    "params": {
        "detail_type": "group",
        "group_id": "12467",
        "message": [
            {
                "type": "text",
                "data": {
                    "text": "我是文字巴拉巴拉巴拉"
                }
            }
        ]
    }
}
```

@tab 响应示例
```json
{
    "status": "ok",
    "retcode": 0,
    "data": true,
    "message": ""
}
```

@tab 在nb2使用
```python
from nonebot.adapters.onebot.v12 import Bot, MessageSegment
from nonebot import get_bot

async def test():
    bot = get_bot()
    message = MessageSegment.text("我是文字巴拉巴拉巴拉") +
              MessageSegment.image(file_id="asd-asd-asd-ads")
    await bot.send_message(detail_type="group",group_id="12467",message=message)

```

:::

## 撤回消息<Badge text="标准" type="success" />
action: `delete_message`
:::danger Wechat
未实现该动作。
:::
