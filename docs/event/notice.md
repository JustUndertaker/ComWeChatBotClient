# 通知事件
:::tip Onebot12
本页所定义的事件均基于[OneBot Connect - 事件](https://12.onebot.dev/connect/data-protocol/event/)，其中 type 字段值应为 `notice`。
:::

## `friend_increase` 好友增加<Badge text="标准" type="success" />
本事件在好友增加时触发
|    字段名    | 数据类型 |        说明         |
| :----------: | :------: | :-----------------: |
| `detail_type` | string | 为`friend_increase` |
| `user_id` | string | 增加好友的 wxid |

## `friend_decrease` 好友减少<Badge text="标准" type="success" />
本事件在好友减少时触发
:::danger Wechat
由于 `wechat` 的单向好友特性，删除好友时并不会提醒他人，故无法实现
:::

## `private_message_delete` 私聊消息删除<Badge text="标准" type="success" />
本事件在私聊消息被删除时触发
|    字段名    | 数据类型 |        说明         |
| :----------: | :------: | :-----------------: |
| `detail_type` | string | 为`private_message_delete` |
| `message_id` | string | 撤回消息ID |
| `user_id` | string | 消息发送者 ID |

## `group_member_increase` 群成员增加<Badge text="标准" type="success" />
