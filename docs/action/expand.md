# 拓展动作

## 获取公众号列表<Badge text="拓展" type="danger" />
action: `wx.get_public_account_list`

:::tabs

@tab 请求参数
无

@tab 响应数据
list[map[string, string]]，每个元素为一个公众号的信息，包含以下字段：

| 字段名    | 数据类型 |    说明    |
| :-------: | :------: | :--------: |
| `user_id` | string | 公众号的wxid |
| `user_name` | string  | 公众号的名称 |
| `wx_number` | string  | 公众号的微信号 |

@tab 请求示例
```json
{
    "action": "wx.get_public_account_list",
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
            "user_id": "gh_3c884a361561",
            "user_name": "微信支付",
            "wx_number": "xxxx",
        },
        {
            "user_id": "gh_3c884a361561",
            "user_name": "微信支付",
            "wx_number": "xxxx",
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
    public_account_list = await bot.call_api("wx.get_public_account_list")

```

:::

## 关注公众号<Badge text="拓展" type="danger" />
action: `wx.follow_public_account`

:::tabs

@tab 请求参数
| 字段名    | 数据类型 |    说明    |
| :-------: | :------: | :--------: |
| `user_id` | string | 公众号的wxid |

@tab 响应数据
无

@tab 请求示例
```json
{
    "action": "wx.follow_public_account",
    "params": {
        "user_id": "gh_3c884a361561"
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
    await bot.call_api("wx.follow_public_account", user_id="gh_3c884a361561")

```

:::

## 通过备注搜索联系人<Badge text="拓展" type="danger" />
action: `wx.search_contact_by_remark`

:::tabs

@tab 请求参数
| 字段名    | 数据类型 |    说明    |
| :-------: | :------: | :--------: |
| `remark` | string | 联系人的备注 |

@tab 响应数据
与 `get_user_info` 一致。

@tab 请求示例
```json
{
    "action": "wx.search_contact_by_remark",
    "params": {
        "remark": "小明"
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
    user_info = await bot.call_api("wx.search_contact_by_remark", remark="小明")

```

:::

## 通过微信号搜索联系人<Badge text="拓展" type="danger" />
action: `wx.search_contact_by_wxnumber`

:::tabs

@tab 请求参数
| 字段名    | 数据类型 |    说明    |
| :-------: | :------: | :--------: |
| `wx_number` | string | 联系人的微信号 |

@tab 响应数据
与 `get_user_info` 一致。

@tab 请求示例
```json
{
    "action": "wx.search_contact_by_wxnumber",
    "params": {
        "wx_number": "nb2"
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
    user_info = await bot.call_api("wx.search_contact_by_wxnumber", wx_number="xiaoming")

```

:::

## 通过昵称搜索联系人<Badge text="拓展" type="danger" />
action: `wx.search_contact_by_nickname`

:::tabs

@tab 请求参数
| 字段名    | 数据类型 |    说明    |
| :-------: | :------: | :--------: |
| `nickname` | string | 联系人的昵称 |

@tab 响应数据
与 `get_user_info` 一致。

@tab 请求示例
```json
{
    "action": "wx.search_contact_by_nickname",
    "params": {
        "nickname": "小明"
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
    user_info = await bot.call_api("wx.search_contact_by_nickname", nickname="小明")

```

:::

## 检测好友状态<Badge text="拓展" type="danger" />
action: `wx.check_friend_status`

:::tabs

@tab 请求参数
| 字段名    | 数据类型 |    说明    |
| :-------: | :------: | :--------: |
| `user_id` | string | 联系人的wxid |

@tab 响应数据
返回`int`，状态如下:
 - `0x00`: Unknown
 - `0xB0`: 被删除
 - `0xB1`: 是好友
 - `0xB2`: 已拉黑
 - `0xB5`: 被拉黑

@tab 请求示例
```json
{
    "action": "wx.check_friend_status",
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
    "data": 0,
    "message": ""
}
```

@tab 在nb2使用
```python
from nonebot.adapters.onebot.v12 import Bot, MessageSegment
from nonebot import get_bot

async def test():
    bot = get_bot()
    status = await bot.call_api("wx.check_friend_status", user_id="1234567")

```

:::

## 获取数据库句柄和表信息<Badge text="拓展" type="danger" />
action: `wx.get_db_info`

:::tabs

@tab 请求参数
无

@tab 响应数据

返回为一个`dict`，key为数据库名，value为database

数据库列表如下:
| 数据库名    | 数据类型 |    说明    |
| :-------: | :------: | :--------: |
| `MicroMsg.db` |  database | 微信数据库 |
| `ChatMsg.db` |  database | 聊天记录数据库 |
| `Misc.db` |  database | 其他数据库 |
| `Media.db` |  database | 媒体数据库 |
| `Emotion.db` |  database | 表情数据库 |
| `FunctionMsg.db` |  database | 功能数据库 |
| `PublicMsg.db` |  database | 公众号数据库 |
| `PublicMsgMedia.db` |  database | 公众号媒体数据库 |
| `MediaMSG0.db` |  database | 媒体数据库 |
| `MSG0.db` |  database | 聊天记录数据库 |
| `OpenIMContact.db` |  database | OpenIM数据库 |
| `OpenIMMsg.db` |  database | OpenIM数据库 |
| `OpenIMMedia.db` |  database | OpenIM数据库 |
| `Sns.db` |  database | 朋友圈数据库 |
| `Favorite.db` |  database | 收藏数据库 |

database定义如下:
| 字段名    | 数据类型 |    说明    |
| :-------: | :------: | :--------: |
| `Handle` | int | 数据库句柄 |
| `tables` | dict | 表信息 |

tables定义如下:
| 字段名    | 数据类型 |    说明    |
| :-------: | :------: | :--------: |
| `name` | string | 表名 |
| `tbl_name` | string | 表名 |
| `root_page` | int | 根页 |
| `sql` | string | 建表语句 |

@tab 请求示例
```json
{
    "action": "wx.get_db_info",
    "params": {}
}
```

@tab 响应示例
```json
{
    "status": "ok",
    "retcode": 0,
    "data": {
        "MicroMsg.db": {
            "Handle": 92852680,
            "tables": [
                {
                    "name": "OpLog",
                    "tbl_name": "OpLog",
                    "root_page": "5",
                    "sql": "CREATE TABLE OpLog(ID INTEGER PRIMARY KEY,CMDItemBuffer BLOB)"
                },
                {
                    "name": "AppInfo",
                    "tbl_name": "AppInfo",
                    "root_page": "9",
                    "sql": "CREATE TABLE AppInfo(InfoKey TEXT PRIMARY KEY,AppId TEXT,Version INT,IconUrl TEXT,StoreUrl TEXT,WatermarkUrl TEXT,HeadImgBuf BLOB,Name TEXT,Description TEXT,Name4EnUS TEXT,Description4EnUS TEXT,Name4ZhTW TEXT,Description4ZhTW TEXT)"
                }
            ]
        },
        "MicroMsg.db": {
            "Handle": 92852680,
            "tables": [
                {
                    "name": "OpLog",
                    "tbl_name": "OpLog",
                    "root_page": "5",
                    "sql": "CREATE TABLE OpLog(ID INTEGER PRIMARY KEY,CMDItemBuffer BLOB)"
                },
                {
                    "name": "AppInfo",
                    "tbl_name": "AppInfo",
                    "root_page": "9",
                    "sql": "CREATE TABLE AppInfo(InfoKey TEXT PRIMARY KEY,AppId TEXT,Version INT,IconUrl TEXT,StoreUrl TEXT,WatermarkUrl TEXT,HeadImgBuf BLOB,Name TEXT,Description TEXT,Name4EnUS TEXT,Description4EnUS TEXT,Name4ZhTW TEXT,Description4ZhTW TEXT)"
                }
            ]
        }
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
    db = await bot.call_api("wx.get_db_info")

```

:::


## 执行SQL语句<Badge text="拓展" type="danger" />
action: `wx.execute_sql`

:::tabs

@tab 请求参数
| 字段名    | 数据类型 |    说明    |
| :-------: | :------: | :--------: |
| `handle` | int | 数据库句柄 |
| `sql` | string | SQL语句 |

@tab 响应数据
sql的响应

@tab 请求示例
```json
{
    "action": "wx.execute_sql",
    "params": {
        "handle": 92852680,
        "sql": "select * from AppInfo"
    }
}
```

@tab 响应示例
```json
{
    "status": "ok",
    "retcode": 0,
    "data":
        {
            "InfoKey": "com.tencent.mm",
            "AppId": "wx7fa037cc7dfabad5",
            "Version": 0,
            "IconUrl": "http://weixin.qq.com/cgi-bin/readtemplate?t=weixin_faq&lang=zh_CN&faq=faq_1_1",
            "StoreUrl": "http://weixin.qq.com/cgi-bin/readtemplate?t=weixin_faq&lang=zh_CN&faq=faq_1_1",
            "WatermarkUrl": "http://weixin.qq.com/cgi-bin/readtemplate?t=weixin_faq&lang=zh_CN&faq=faq_1_1",
            "HeadImgBuf": null,
            "Name": "微信",
            "Description": "微信",
            "Name4EnUS": "WeChat",
            "Description4EnUS": "WeChat",
            "Name4ZhTW": "微信",
            "Description4ZhTW": "微信"
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
    db = await bot.call_api("wx.get_db_info")
    for db_name, db_info in db.items():
        if db_name == "MicroMsg.db":
            sql = await bot.call_api("wx.execute_sql", handle=db_info["Handle"], sql="select * from AppInfo")
            print(sql)

```

:::

## 备份数据库<Badge text="拓展" type="danger" />
action: `wx.backup_db`

:::warning 注意
`file_path`需要填写绝对路径+保存的文件名

由于Com通信只能在主线程，所以此操作会卡事件循环，导致Client无法响应其他请求，所以此Action不要经常使用
:::

:::tabs

@tab 请求参数
| 字段名    | 数据类型 |    说明    |
| :-------: | :------: | :--------: |
| `handle` | int | 数据库句柄 |
| `file_path` | string | 文件路径 |

@tab 响应数据
无

@tab 请求示例
```json
{
    "action": "wx.backup_db",
    "params": {
        "handle": 92852680,
        "file_path": "C:\\Users\\Administrator\\Desktop\\test.db"
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
    db = await bot.call_api("wx.get_db_info")
    for db_name, db_info in db.items():
        if db_name == "MicroMsg.db":
            await bot.call_api("wx.backup_db", handle=db_info["Handle"], file_path="C:\\Users\\Administrator\\Desktop\\test.db")

```

:::

## 通过好友请求<Badge text="拓展" type="danger" />
action: `wx.accept_friend`

:::tabs

@tab 请求参数
| 字段名    | 数据类型 |    说明    |
| :-------: | :------: | :--------: |
| `v3` | string | v3数据，通过 `wx.friend_request` 事件获得 |
| `v4` | string | v4数据，通过 `wx.friend_request` 事件获得 |

@tab 响应数据
无

@tab 请求示例
```json
{
    "action": "wx.accept_friend",
    "params": {
        "v3": "v3数据",
        "v4": "v4数据"
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
    await bot.call_api("wx.accept_friend", v3="v3数据", v4="v4数据")

```

:::

## 获取微信版本<Badge text="拓展" type="danger" />
action: `wx.get_wechat_version`

:::tabs

@tab 请求参数
无

@tab 响应数据
`string`: 微信版本

@tab 请求示例
```json
{
    "action": "wx.get_wechat_version",
    "params": {}
}
```

@tab 响应示例
```json
{
    "status": "ok",
    "retcode": 0,
    "data": "3.7.0.30",
    "message": ""
}
```

@tab 在nb2使用
```python
from nonebot.adapters.onebot.v12 import Bot, MessageSegment
from nonebot import get_bot

async def test():
    bot = get_bot()
    version = await bot.call_api("wx.get_wechat_version")
    print(version)

```

:::

## 设置微信版本号<Badge text="拓展" type="danger" />
action: `wx.set_wechat_version`

自定义微信版本号，一定程度上防止自动更新
:::tip Wechat
微信版本号格式类似为`3.7.0.26`
:::

:::tabs

@tab 请求参数
| 字段名    | 数据类型 |    说明    |
| :-------: | :------: | :--------: |
| `version` | string | 微信版本号 |

@tab 响应数据
无

@tab 请求示例
```json
{
    "action": "wx.set_wechat_version",
    "params": {
        "version": "3.7.0.26"
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
    await bot.call_api("wx.set_wechat_version", version="3.7.0.26")

```

:::

## 删除好友<Badge text="拓展" type="danger" />
action: `wx.delete_friend`

:::tabs

@tab 请求参数
| 字段名    | 数据类型 |    说明    |
| :-------: | :------: | :--------: |
| `user_id` | string | 好友wxid |

@tab 响应数据
无

@tab 请求示例
```json
{
    "action": "wx.delete_friend",
    "params": {
        "user_id": "wxid_xxxxx"
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
    await bot.call_api("wx.delete_friend", user_id="wxid_xxxxx")

```

:::

## 修改好友或群聊备注<Badge text="拓展" type="danger" />
action: `wx.set_remark`

:::tabs

@tab 请求参数
| 字段名    | 数据类型 |    说明    |
| :-------: | :------: | :--------: |
| `user_id` | string | 好友或群聊wxid |
| `remark` | string | 备注 |

@tab 响应数据
无

@tab 请求示例
```json
{
    "action": "wx.set_remark",
    "params": {
        "user_id": "wxid_xxxxx",
        "remark": "备注"
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
    await bot.call_api("wx.set_remark", user_id="wxid_xxxxx", remark="备注")

```

:::

## 设置群公告<Badge text="拓展" type="danger" />
action: `wx.set_group_announcement`

:::warning 注意权限
请确认具有相关权限再调用。
:::

:::tabs

@tab 请求参数
| 字段名    | 数据类型 |    说明    |
| :-------: | :------: | :--------: |
| `group_id` | string | 群聊wxid |
| `announcement` | string | 公告 |

@tab 响应数据
无

@tab 请求示例
```json
{
    "action": "wx.set_group_announcement",
    "params": {
        "group_id": "wxid_xxxxx",
        "announcement": "公告"
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
    await bot.call_api("wx.set_group_announcement", group_id="wxid_xxxxx", announcement="公告")

```

:::

## 设置群昵称<Badge text="拓展" type="danger" />
action: `wx.set_group_nickname`

:::tabs

@tab 请求参数
| 字段名    | 数据类型 |    说明    |
| :-------: | :------: | :--------: |
| `group_id` | string | 群聊 ID |
| `nickname` | string | 昵称 |

@tab 响应数据
无

@tab 请求示例
```json
{
    "action": "wx.set_group_nickname",
    "params": {
        "group_id": "wxid_xxxxx",
        "nickname": "昵称"
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
    await bot.call_api("wx.set_group_nickname", group_id="wxid_xxxxx", nickname="昵称")

```

:::

## 获取群成员昵称<Badge text="拓展" type="danger" />
action: `wx.get_groupmember_nickname`

:::tabs

@tab 请求参数
| 字段名    | 数据类型 |    说明    |
| :-------: | :------: | :--------: |
| `group_id` | string | 群聊 ID |
| `user_id` | string | 群成员 ID |

@tab 响应数据
`str` : 群成员昵称

@tab 请求示例
```json
{
    "action": "wx.get_groupmember_nickname",
    "params": {
        "group_id": "wxid_xxxxx",
        "user_id": "wxid_xxxxx"
    }
}
```

@tab 响应示例
```json
{
    "status": "ok",
    "retcode": 0,
    "data": "昵称",
    "message": ""
}
```

@tab 在nb2使用
```python
from nonebot.adapters.onebot.v12 import Bot, MessageSegment
from nonebot import get_bot

async def test():
    bot = get_bot()
    nickname = await bot.call_api("wx.get_groupmember_nickname", group_id="wxid_xxxxx", user_id="wxid_xxxxx")

```

:::

## 删除群成员<Badge text="拓展" type="danger" />
action: `wx.delete_groupmember`

:::warning 注意权限
请确认具有相关权限再调用。
:::

:::tabs

@tab 请求参数
| 字段名    | 数据类型 |    说明    |
| :-------: | :------: | :--------: |
| `group_id` | string | 群聊 ID |
| `user_list` | str/list[str] | 群成员 ID，支持列表删除 |

@tab 响应数据
无

@tab 请求示例
```json
{
    "action": "wx.delete_groupmember",
    "params": {
        "group_id": "wxid_xxxxx",
        "user_list": "wxid_xxxxx"
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
    await bot.call_api("wx.delete_groupmember", group_id="wxid_xxxxx", user_list="wxid_xxxxx")

```

:::

## 添加群成员<Badge text="拓展" type="danger" />
action: `wx.add_groupmember`

:::warning 注意权限
请确认具有相关权限再调用。
:::

:::tabs

@tab 请求参数
| 字段名    | 数据类型 |    说明    |
| :-------: | :------: | :--------: |
| `group_id` | string | 群聊 ID |
| `user_list` | str/list[str] | 群成员 ID，支持列表添加 |

@tab 响应数据
无

@tab 请求示例
```json
{
    "action": "wx.add_groupmember",
    "params": {
        "group_id": "wxid_xxxxx",
        "user_list": "wxid_xxxxx"
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
    await bot.call_api("wx.add_groupmember", group_id="wxid_xxxxx", user_list="wxid_xxxxx")

```

:::

## 获取公众号历史消息<Badge text="拓展" type="danger" />
action: `wx.get_public_history`

一次获取十条推送记录，可通过 offset 参数调节。
:::tabs

@tab 请求参数
| 字段名    | 数据类型 |    说明    |
| :-------: | :------: | :--------: |
| `public_id` | string | 公众号 ID |
| `offset` | int | 起始偏移，为空的话则从新到久获取十条，该值可从返回数据中取得 |

@tab 响应数据
`list` : 消息列表

@tab 请求示例
```json
{
    "action": "wx.get_public_history",
    "params": {
        "public_id": "wxid_xxxxx",
        "offset": 0
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
            "title": "标题",
            "content": "内容",
            "url": "链接",
            "time": 1620000000
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
    history = await bot.call_api("wx.get_public_history", public_id="wxid_xxxxx", offset=0)

```

:::

## 转发消息<Badge text="拓展" type="danger" />
action: `wx.send_forward_msg`

只支持单条转发
:::tabs

@tab 请求参数
| 字段名    | 数据类型 |    说明    |
| :-------: | :------: | :--------: |
| `user_id` | string | 用户 ID |
| `message_id` | string | 消息 ID |

@tab 响应数据
无

@tab 请求示例
```json
{
    "action": "wx.send_forward_msg",
    "params": {
        "user_id": "wxid_xxxxx",
        "message_id": "wxid_xxxxx"
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
    await bot.call_api("wx.send_forward_msg", user_id="wxid_xxxxx", message_id="wxid_xxxxx")

```

:::

## 发送原始xml消息<Badge text="拓展" type="danger" />
action: `wx.send_raw_xml`

:::tabs

@tab 请求参数
| 字段名    | 数据类型 |    说明    |
| :-------: | :------: | :--------: |
| `user_id` | string | 用户 ID |
| `xml` | string | xml消息 |
| `image_path` | string | 图片路径，可选 |

@tab 响应数据
无

@tab 请求示例
```json
{
    "action": "wx.send_raw_xml",
    "params": {
        "user_id": "wxid_xxxxx",
        "xml": "<xml>...</xml>",
        "image_path": "C:\\Users\\xxx\\Pictures\\xxx.jpg"
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
    await bot.call_api("wx.send_raw_xml", user_id="wxid_xxxxx", xml="<xml>...</xml>")

```

:::

## 发送名片<Badge text="拓展" type="danger" />
action: `wx.send_card`

:::tabs

@tab 请求参数
| 字段名    | 数据类型 |    说明    |
| :-------: | :------: | :--------: |
| `user_id` | string | 用户 ID |
| `card_id` | string | 名片 ID |
| `nickname` | string | 名片昵称 |

@tab 响应数据
无

@tab 请求示例
```json
{
    "action": "wx.send_card",
    "params": {
        "user_id": "wxid_xxxxx",
        "card_id": "wxid_xxxxx",
        "nickname": "昵称"
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
    await bot.call_api("wx.send_card", user_id="wxid_xxxxx", card_id="wxid_xxxxx", nickname="昵称")

```

:::

## 清理文件缓存<Badge text="拓展" type="danger" />
action: `wx.clean_cache`

:::tabs

@tab 请求参数
| 字段名    | 数据类型 |    说明    |
| :-------: | :------: | :--------: |
| `days` | int | 清理多少天前的缓存 |

@tab 响应数据
`int` : 清理的文件数量

@tab 请求示例
```json
{
    "action": "wx.clean_cache",
    "params": {
        "days": 7
    }
}
```

@tab 响应示例
```json
{
    "status": "ok",
    "retcode": 0,
    "data": 10,
    "message": ""
}
```

@tab 在nb2使用
```python
from nonebot.adapters.onebot.v12 import Bot, MessageSegment
from nonebot import get_bot

async def test():
    bot = get_bot()
    await bot.call_api("wx.clean_cache", days=7)

```

:::
