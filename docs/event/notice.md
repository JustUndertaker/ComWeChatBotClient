# 通知事件
:::tip Onebot12
本页所定义的事件均基于[OneBot Connect - 事件](https://12.onebot.dev/connect/data-protocol/event/)，其中 type 字段值应为 `notice`。
:::

## 好友增加<Badge text="标准" type="success" />
本事件在好友增加时触发
:::danger Wechat
wechat 在添加好友时使用发送消息："我通过了你的朋友验证请求，现在我们可以开始聊天了"等，故这边不好实现
:::

## 好友减少<Badge text="标准" type="success" />
本事件在好友减少时触发
:::danger Wechat
由于 `wechat` 的单向好友特性，删除好友时并不会提醒他人，故无法实现
:::

## 私聊消息删除<Badge text="标准" type="success" />
本事件在私聊消息被删除时触发
|    字段名    | 数据类型 |        说明         |
| :----------: | :------: | :-----------------: |
| `detail_type` | string | `private_message_delete` |
| `message_id` | string | 撤回消息ID |
| `user_id` | string | 消息发送者 ID |

## 群成员增加<Badge text="标准" type="success" />
本事件应在群成员（包括机器人自身）申请加群通过、被邀请进群或其它方式进群时触发
:::danger Wechat
暂未实现
:::

## 群成员减少<Badge text="标准" type="success" />
本事件应在群成员（包括机器人自身）主动退出、被踢出或其它方式退出时触发
:::danger Wechat
暂未实现
:::

## 群消息删除<Badge text="标准" type="success" />
本事件应在群消息被撤回或被管理员删除时触发
|    字段名    | 数据类型 |        说明         |
| :----------: | :------: | :-----------------: |
| `detail_type` | string | `group_message_delete` |
| `sub_type` | string | 为 `delete` |
| `group_id` | string | 群 ID |
| `message_id` | string | 消息 ID |
| `user_id` | string | 消息发送者 ID |
| `operator_id` | string | 为空 |

## 私聊接收文件通知<Badge text="拓展" type="danger" />
在接收到文件时会发送通知（此时文件还未下载）
|    字段名    | 数据类型 |        说明         |
| :----------: | :------: | :-----------------: |
| `detail_type` | string | `wx.get_private_file` |
| `file_name` | string | 文件名 |
| `file_length` | int | 文件长度 |
| `md5` | string | 文件md5值 |
| `user_id` | string | 发送方 ID |

## 群聊接收文件通知<Badge text="拓展" type="danger" />
在接收到文件时会发送通知（此时文件还未下载）
|    字段名    | 数据类型 |        说明         |
| :----------: | :------: | :-----------------: |
| `detail_type` | string | `wx.get_private_file` |
| `file_name` | string | 文件名 |
| `file_length` | int | 文件长度 |
| `md5` | string | 文件md5值 |
| `group_id` | string | 群 ID |
| `user_id` | string | 发送方 ID |

## 私聊收到红包通知<Badge text="拓展" type="danger" />
私聊收到红包时的通知
|    字段名    | 数据类型 |        说明         |
| :----------: | :------: | :-----------------: |
| `detail_type` | string | `wx.get_private_redbag` |
| `user_id` | string | 发送方 ID |

## 群聊收到红包通知<Badge text="拓展" type="danger" />
群聊收到红包时的通知
|    字段名    | 数据类型 |        说明         |
| :----------: | :------: | :-----------------: |
| `detail_type` | string | `wx.get_group_redbag` |
| `group_id` | string | 群 ID |
| `user_id` | string | 发送方 ID |

## 私聊拍一拍通知<Badge text="拓展" type="danger" />
私聊拍一拍时通知
|    字段名    | 数据类型 |        说明         |
| :----------: | :------: | :-----------------: |
| `detail_type` | string | `wx.get_private_poke` |
| `user_id` | string | 接收方 ID |
| `from_user_id` | string | 发送方 ID |

## 群聊拍一拍通知<Badge text="拓展" type="danger" />
群聊拍一拍时通知
|    字段名    | 数据类型 |        说明         |
| :----------: | :------: | :-----------------: |
| `detail_type` | string | `wx.get_group_poke` |
| `group_id` | string | 群 ID |
| `user_id` | string | 接收方 ID |
| `from_user_id` | string | 发送方 ID |

## 私聊获取名片通知<Badge text="拓展" type="danger" />
私聊收到名片时通知
|    字段名    | 数据类型 |        说明         |
| :----------: | :------: | :-----------------: |
| `detail_type` | string | `wx.get_private_card` |
| `user_id` | string | 发送方 ID |
| `v3` | string | 名片v3信息 |
| `v4` | string | 名片v4信息 |
| `nickname` | string | 名片昵称 |
| `head_url` | string | 头像url |
| `province` | string | 省 |
| `city` | string | 市 |
| `sex` | string | 性别 |

## 群聊获取名片通知<Badge text="拓展" type="danger" />
群聊收到名片时通知
|    字段名    | 数据类型 |        说明         |
| :----------: | :------: | :-----------------: |
| `detail_type` | string | `wx.get_group_card` |
| `group_id` | string | 群 ID |
| `user_id` | string | 发送方 ID |
| `v3` | string | 名片v3信息 |
| `v4` | string | 名片v4信息 |
| `nickname` | string | 名片昵称 |
| `head_url` | string | 头像url |
| `province` | string | 省 |
| `city` | string | 市 |
| `sex` | string | 性别 |
