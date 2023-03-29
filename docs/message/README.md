# 消息段
本项目目前实现了部分标准消息段及拓展消息段
:::tip onebot12
`消息段:` 表示聊天消息的一个部分，在一些平台上，聊天消息支持图文混排，其中就会有多个消息段，分别表示每个图片和每段文字。
:::

## 纯文本<Badge text="标准" type="success" />
type: `text`

表示一段纯文本。
 - [x] 可以接收
 - [x] 可以发送

::: tabs
@tab 参数
| 字段名    | 数据类型 | 说明       |
| :-------: | :------: | :--------: |
| `text`    | string   | 纯文本内容 |

@tab 示例
```json
{
    "type": "text",
    "data": {
        "text": "这是一个纯文本"
    }
}
```

@tab nb2使用
``` python
from nonebot.adapters.onebot.v12 import MessageSegment

message = MessageSegment.text("这是一个纯文本")
```
:::
## 提及（即 @）<Badge text="标准" type="success" />
type: `mention`

表示at某人。

::: warning 注意场景

此消息段只有在群聊时才可使用

:::

- [x] 可以接收
- [x] 可以发送

::: tabs

@tab 参数

|  字段名   | 数据类型 |     说明     |
| :-------: | :------: | :----------: |
| `user_id` |  string  | 提及用户的id |

@tab 示例

```json
{
    "type": "mention",
    "data": {
        "user_id": "1234567"
    }
}
```

@tab nb2使用
```python
from nonebot.adapters.onebot.v12 import MessageSegment

message = MessageSegment.mention(user_id="123456")
```

:::

## 提及所有人<Badge text="标准" type="success" />
type: `mention_all`

表示at所有人。

::: danger 注意权限

没有at所有人权限，请不要尝试发送此消息段

:::

- [x] 可以接收
- [x] 可以发送

::: tabs

@tab 参数

无。

@tab 示例

```json
{
    "type": "mention_all",
    "data": {}
}
```

@tab nb2使用
```python
from nonebot.adapters.onebot.v12 import MessageSegment

message = MessageSegment.mention_all()
```

:::

## 图片<Badge text="标准" type="success" />
type:`image`

表示一张图片。

- [x] 可以接收
- [x] 可以发送

::: tabs

@tab 参数

|  字段名   | 数据类型 |    说明     |
| :-------: | :------: | :---------: |
| `file_id` |  string  | 图片文件 ID |

@tab 示例

```json
{
    "type": "image",
    "data": {
        "file_id": "e30f9684-3d54-4f65-b2da-db291a477f16"
    }
}
```

@tab nb2使用
```python
from nonebot.adapters.onebot.v12 import MessageSegment

message = MessageSegment.image(file_id="e30f9684-3d54-4f65-b2da-db291a477f16")
```

:::

## 语音<Badge text="标准" type="success" />
type: `voice`

表示一段语音消息。

- [x] 可以接收
- [ ] 可以发送

::: tabs

@tab 参数

|  字段名   | 数据类型 |    说明     |
| :-------: | :------: | :---------: |
| `file_id` |  string  | 语音文件 ID |

@tab 示例

```json
{
    "type": "voice",
    "data": {
        "file_id": "e30f9684-3d54-4f65-b2da-db291a477f16"
    }
}
```



:::

## 音频<Badge text="标准" type="success" />
type: `audio`

音频文件。

::: warning 未实现

本应用未实现此字段

:::

## 视频<Badge text="标准" type="success" />
type: `video`

视频消息

- [x] 可以接收
- [ ] 可以发送

:::tabs

@tab 参数

|  字段名   | 数据类型 |    说明     |
| :-------: | :------: | :---------: |
| `file_id` |  string  | 视频文件 ID |

@tab 示例

```json
{
    "type": "video",
    "data": {
        "file_id": "e30f9684-3d54-4f65-b2da-db291a477f16"
    }
}
```



:::

## 文件<Badge text="标准" type="success" />
type: `file`

文件消息

- [x] 可以接收
- [x] 可以发送

:::tabs

@tab 参数

|  字段名   | 数据类型 |    说明     |
| :-------: | :------: | :---------: |
| `file_id` |  string  |     文件 ID |

@tab 示例

```json
{
    "type": "file",
    "data": {
        "file_id": "e30f9684-3d54-4f65-b2da-db291a477f16"
    }
}
```

@tab nb2使用
```python
from nonebot.adapters.onebot.v12 import MessageSegment

message = MessageSegment.file(file_id="e30f9684-3d54-4f65-b2da-db291a477f16")
```

:::

## 位置<Badge text="标准" type="success" />
type: `location`

位置消息。

- [x] 可以接收
- [ ] 可以发送

::: tabs

@tab 参数

|   字段名    | 数据类型 |   说明   |
| :---------: | :------: | :------: |
| `latitude`  | float64  |   纬度   |
| `longitude` | float64  |   经度   |
|   `title`   |  string  |   标题   |
|  `content`  |  string  | 地址内容 |

@tab 示例

```json
{
    "type": "location",
    "data": {
        "latitude": 31.032315,
        "longitude": 121.447127,
        "title": "上海交通大学闵行校区",
        "content": "中国上海市闵行区东川路800号"
    }
}
```

:::



## 回复<Badge text="标准" type="success" />
type: `reply`

回复消息。

:::info wechat

在微信里，为引用消息

:::

- [x] 可以接收
- [ ] 可以发送

::: tabs

@tab 参数

|    字段名    | 数据类型 |        说明         |
| :----------: | :------: | :-----------------: |
| `message_id` |  string  |    回复的消息 ID    |
|  `user_id`   |  string  | 回复的消息发送者 ID |

@tab 示例

```json
{
    "type": "reply",
    "data": {
        "message_id": "6283",
        "user_id": "1234567"
    }
}
```



:::

## 表情<Badge text="拓展" type="danger" />
type: `wx.emoji`

表示表情消息

::: warning 与图片区别
在微信里，图片消息指直接发送图片；而表情为动态gif表情包等
:::
 - [x] 可以接收
 - [x] 可以发送
::: tabs

@tab 参数

|  字段名   | 数据类型 |    说明     |
| :-------: | :------: | :---------: |
| `file_id` |  string  | 图片文件 ID |

@tab 示例

```json
{
    "type": "wx.emoji",
    "data": {
        "file_id": "e30f9684-3d54-4f65-b2da-db291a477f16"
    }
}
```

@tab nb2使用
```python
from nonebot.adapters.onebot.v12 import MessageSegment

message = MessageSegment("wx.emoji",{"file_id":"e30f9684-3d54-4f65-b2da-db291a477f16"})
```

:::

## 链接<Badge text="拓展" type="danger" />
type: `wx.link`

文章链接消息
 - [x] 可以接收
 - [x] 可以发送
::: tabs

@tab 参数

|  字段名   | 数据类型 |    说明     |
| :-------: | :------: | :---------: |
| `title` |  string  | 文章标题 |
| `des` |  string  | 消息卡片摘要 |
| `url` |  string  | 文章链接 |
| `file_id` |  可选,string  | 消息图片id |

@tab 示例

```json
{
    "type": "wx.link",
    "data": {
        "title": "发一篇文章",
        "des": "你干嘛，哎哟",
        "url": "http://www.baidu.com",
        "file_id": "e30f9684-3d54-4f65-b2da-db291a477f16"
    }
}
```

@tab nb2使用
```python
from nonebot.adapters.onebot.v12 import MessageSegment

message = MessageSegment("wx.link",{
        "title": "发一篇文章",
        "des": "你干嘛，哎哟",
        "url": "http://www.baidu.com",
        "file_id": "e30f9684-3d54-4f65-b2da-db291a477f16"
        })
```

:::
## 小程序<Badge text="拓展" type="danger" />
type: `wx.app`

小程序消息
 - [x] 可以接收
 - [ ] 可以发送

::: tabs

@tab 参数

|    字段名    | 数据类型 |        说明         |
| :----------: | :------: | :-----------------: |
| `appid` |  string  |    小程序id    |
|  `title`   |  string  | 消息标题 |
|  `url`   |  string  | 链接地址 |

@tab 示例

```json
{
    "type": "wx.app",
    "data": {
        "appid": "abcd",
        "title": "肯德基疯狂星期四",
        "url": "http://www.baidu.com"
    }
}
```



:::
