# 请求事件
:::tip Onebot12
本页所定义的事件均基于 [OneBot Connect - 事件](https://12.onebot.dev/connect/data-protocol/event/)，其中 type 字段值应为 `request`。
:::

## 添加好友请求<Badge text="拓展" type="danger" />
他人请求添加好友时上报

|    字段名    | 数据类型 |        说明         |
| :----------: | :------: | :-----------------: |
| `detail_type` | string | `wx.friend_request` |
| `user_id` | string | 发送方的 `wxid` |
| `v3` | string | 事件请求v3，接收请求时使用 |
| `v4` | string | 事件请求v4，接收请求时使用 |
| `nickname` | string | 请求人昵称 |
| `content` | string | 附加的话 |
| `country` | string | 国家 |
| `province` | string | 省份 |
| `city` | string | 城市 |
