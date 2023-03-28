# 消息事件
:::tip Onebot12
本页所定义的事件均基于 [OneBot Connect - 事件](https://12.onebot.dev/connect/data-protocol/event/)，其中 type 字段值应为 `message`。
:::

## 私聊消息<Badge text="标准" type="success" />

|    字段名    | 数据类型 |        说明         |
| :----------: | :------: | :-----------------: |
| `detail_type` | string | `private` |
| `message_id` | string | 消息唯一 ID |
| `message` | message | 消息内容，消息段列表 |
| `alt_message` | string | 消息内容的替代表示 |
| `user_id` | string | 发送方`wxid` |

## 群消息<Badge text="标准" type="success" />

|    字段名    | 数据类型 |        说明         |
| :----------: | :------: | :-----------------: |
| `detail_type` | string | `group` |
| `message_id` | string | 消息唯一 ID |
| `message` | message | 消息内容，消息段列表 |
| `alt_message` | string | 消息内容的替代表示 |
| `group_id` | string | 群id，以`@chatroom`结尾 |
| `user_id` | string | 发送方`wxid` |


