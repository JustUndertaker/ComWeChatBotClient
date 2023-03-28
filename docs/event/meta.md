# 元事件
::: tip Onebot12
Onebot 实现内部自发产生的一类事件，例如心跳等，与 OneBot 本身的运行状态有关，与实现对应的机器人平台无关。
:::
本项目实现了以下的元事件。
## `connect` 连接
对于正向 WebSocket 和反向 WebSocket 通信方式，在连接建立后会推送给应用端
的第一个事件；HTTP 和 HTTP Webhook 通信方式不会产生连接事件。

::: tabs

@tab 字段

|    字段名    | 数据类型 |        说明         |
| :----------: | :------: | :-----------------: |
| `detail_type` | string | 为`connect` |
| `version` | resp[get_version] | OneBot 实现端版本信息，与 get_version 动作响应数据一致|

@tab 示例
```json
{
    "id": "b6e65187-5ac0-489c-b431-53078e9d2bbb",
    "time": 1632847927.599013,
    "type": "meta",
    "detail_type": "connect",
    "sub_type": "",
    "version": {
        "impl": "ComWechat",
        "version": "1.2.0",
        "onebot_version": "12"
    }
}
```

:::

## `heartbeat` 心跳
当 enabled 配置为 true 时，每隔 interval 产生一个心跳事件。
:::tip 配置
间隔 `interval` 对应 `.env` 配置中的 `heartbeat_interval`，单位是ms
:::

::: tabs

@tab 字段

|    字段名    | 数据类型 |        说明         |
| :----------: | :------: | :-----------------: |
| `detail_type` | string | 为 `heartbeat` |
| `interval` | int64 | 到下次心跳的间隔，单位：毫秒 |

@tab 示例

```json
{
    "id": "b6e65187-5ac0-489c-b431-53078e9d2bbb",
    "time": 1632847927.599013,
    "type": "meta",
    "detail_type": "heartbeat",
    "sub_type": "",
    "interval": 5000
}
```

:::

## `status_update` 状态更新
:::danger 未实现
目前没有实现该事件
:::
