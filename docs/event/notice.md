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
