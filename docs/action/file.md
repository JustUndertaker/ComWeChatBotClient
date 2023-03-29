# 文件动作

:::tip bytes数据类型
根据 [Onebot12 - 基本数据类型](https://12.onebot.dev/connect/data-protocol/basic-types/):

> 在 JSON 中表示为 Base64 编码的字符串，MessagePack 中表示为 bin 格式的字节数组。

:::

## 上传文件<Badge text="标准" type="success" />
action: `upload_file`

:::tabs

@tab 请求参数
| 字段名    | 数据类型 |    说明    |
| :-------: | :------: | :--------: |
| `type` | string | 上传文件的方式，为 `url`、`path`、`data` 之一 |
| `name` | string | 文件名 |
| `url` | string | 文件的url，当 `type` 为 `url` 时必填 |
| `headers` | map[string]string | `可选:`下载文件时的请求头 |
| `path` | string | 文件的路径，当 `type` 为 `path` 时必填 |
| `data` | bytes | 文件数据，当 `type` 为 `data` 时必填 |

@tab 响应数据
| 字段名    | 数据类型 |    说明    |
| :-------: | :------: | :--------: |
| `file_id` | string | 文件 ID，可供以后使用 |

@tab 请求示例
```json
{
    "action": "upload_file",
    "params": {
        "type": "url",
        "name": "test.png",
        "url": "https://example.com/test.png"
    }
}
```

@tab 响应示例
```json
{
    "status": "ok",
    "retcode": 0,
    "data": {
        "file_id": "e30f9684-3d54-4f65-b2da-db291a477f16"
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
    file_id = await bot.upload_file(type="url",
                                    name="test.png",
                                    url="https://example.com/test.png"
                                    )

```

:::

## 分片上传文件<Badge text="标准" type="success" />
action: `upload_file_fragmented`

:::danger Wechat
暂未实现
:::

## 获取文件<Badge text="标准" type="success" />
action: `get_file`

:::tabs

@tab 请求参数
| 字段名    | 数据类型 |    说明    |
| :-------: | :------: | :--------: |
| `file_id` | string | 文件 ID |
| `type` | string  | 获取文件的方式，为 `url`、`path`、`data` 之一 |

@tab 响应数据
| 字段名    | 数据类型 |    说明    |
| :-------: | :------: | :--------: |
| `name` | string | 文件名 |
| `url` | string | 文件的url，当 `type` 为 `url` 时返回 |
| `headers` | map[string]string | 为空 |
| `path` | string | 文件的路径，当 `type` 为 `path` 时返回 |
| `data` | bytes | 文件数据，当 `type` 为 `data` 时返回 |

@tab 请求示例
```json
{
    "action": "get_file",
    "params": {
        "file_id": "e30f9684-3d54-4f65-b2da-db291a477f16",
        "type": "url"
    }
}
```

@tab 响应示例
```json
{
    "status": "ok",
    "retcode": 0,
    "data": {
        "name": "test.png",
        "url": "https://example.com/test.png"
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
    file_url = await bot.get_file(file_id="e30f9684-3d54-4f65-b2da-db291a477f16",type="url")

```

:::

## 分片获取文件<Badge text="标准" type="success" />
action: `get_file_fragmented`

:::danger Wechat
暂未实现
:::
