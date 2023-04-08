# 开始
此文档将引导你使用本项目。
## 许可证
本项目采用 [AGPLv3](https://github.com/JustUndertaker/ComWeChatBotClient/blob/main/LICENSE) 许可证
::: danger AGPLv3
本项目不带有主动添加，涉及金钱接口，不鼓励、不支持一切商业使用。
:::
## 上游依赖
本项目依赖上游：[ComWeChatRobot](https://github.com/ljc545w/ComWeChatRobot)。
::: tip ComWeChatRobot
PC微信机器人，实现获取通讯录，发送文本、图片、文件等消息，封装COM接口供Python、C#调用
:::
## 微信版本
本项目使用的微信版本为：3.7.0.30，请安装此版本微信，否则无法使用，下载地址：[传送门](https://github.com/tom-snow/wechat-windows-versions/releases/download/v3.7.0.30/WeChatSetup-3.7.0.30.exe)

安装后想办法禁用升级。
## 安装环境
本项目为PC Hook，并且使用Com接口调用，故只支持Windows系统。为了使用Com接口，在启动本项目时，应首先注册Com服务：
::: tip 以管理员权限执行以下命令
```bat
# 安装
CWeChatRobot.exe /regserver
# 卸载
CWeChatRobot.exe /unregserver
```
:::
或者使用文件下的 `install.bat`、`uninstall.bat`来安装与卸载。
## Onebot12
本项目使用 [Onebot12](https://12.onebot.dev/) 作为协议进行传输数据
::: tip Onebot12
OneBot 是一个聊天机器人应用接口标准，旨在统一不同聊天平台上的机器人应用开发接口，使开发者只需编写一次业务逻辑代码即可应用到多种机器人平台。
:::
目前支持的通信方式:
 - [x] HTTP
 - [X] HTTP Webhook
 - [x] 正向 WebSocket
 - [x] 反向 WebSocket

## 配置
本项目下的 `.env` 文件为项目配置文件，下面讲解配置文件项目。

### `host`
服务Host
 - **类型:** `IPvAnyAddress`
 - **默认值:** `127.0.0.1`

在使用 `http` 和 `正向 websocket` 方式时会监听此host

### `port`
服务端口
 - **类型:** `int`(1~65535)
 - **默认值:** `8000`

在使用 `http` 和 `正向 websocket` 方式时会监听此端口，注意不要和其他端口冲突！

### `access_token`
访问令牌
 - **类型:** `str`
 - **默认值:** `""`

配置了访问令牌后，与本服务通信的另一端也要配置同样的token，否则会连接失败。

### `heartbeat_enabled`
心跳事件
 - **类型:** `bool`
 - **默认值:** `false`

开启心跳后，将周期向连接端发送心跳事件。

### `heartbeat_interval`
心跳间隔
 - **类型:** `int`(1~65535)
 - **默认值:** `5000`

开启心跳后有用，单位毫秒，必须大于0

### `enable_http_api`
开启http访问
 - **类型:** `bool`
 - **默认值:** `true`

是否开启http访问功能。

### `event_enabled`
启用get_latest_events
 - **类型:** `bool`
 - **默认值:** `false`

开启http时有效，是否启用 `get_latest_events` 原动作

### `event_buffer_size`
缓冲区大小
 - **类型:** `int`
 - **默认值:** `0`

`get_latest_events` 存储的事件缓冲区大小，超过该大小将会丢弃最旧的事件，0 表示不限大小

### `enable_http_webhook`
启用http webhook
 - **类型:** `bool`
 - **默认值:** `false`

是否启用http webhook。

### `webhook_url`
上报地址
 - **类型:** `Set(URL)`
 - **默认值:** `["http://127.0.0.1:8080/onebot/v12/http/"]`

启用webhook生效，webhook 上报地址，需要以`http://`开头，多个地址用`,`分隔。

### `webhook_timeout`
上报请求超时时间
 - **类型:** `int`
 - **默认值:** `5000`

启用webhook生效，单位：毫秒，0 表示不超时

### `websocekt_type`
websocket连接方式
 - **类型:** `str`
 - **默认值:** `Unable`

只能是以下值：
 - `Unable` : 不开启websocket连接
 - `Forward` : 正向websocket连接
 - `Backward` : 反向websocket连接

### `websocket_url`
连接地址
 - **类型:** `Set(URL)`
 - **默认值:** `["ws://127.0.0.1:8080/onebot/v12/ws/"]`

反向websocket连接时生效，反向 WebSocket 连接地址，需要以`ws://`或`wss://`开头，多个地址用`,`分隔。

### `reconnect_interval`
重连间隔
 - **类型:** `int`
 - **默认值:** `5000`

反向websocket连接时生效，反向 WebSocket 重连间隔，单位：毫秒，必须大于 0

### `websocket_buffer_size`
缓冲区大小
 - **类型** `int`
 - **默认值** `4`

反向websocket连接时生效，反向 WebSocket 缓冲区大小，单位：mb，必须大于 0

### `log_level`
日志等级
 - **类型:** `str`
 - **默认值:** `INFO`

一般为以下值：
 - `INFO` : 正常使用
 - `DEBUG` : debug下使用

### `log_days`
保存天数
 - **类型:** `int`
 - **默认值:** `10`

日志保存天数。

### `cache_days`
缓存天数
 - **类型:** `int`
 - **默认值:** `0`

临时文件缓存天数，为0则不清理缓存

## 使用 Nonebot2
本项目支持与 [Nonebot2](https://v2.nonebot.dev/) 进行通信，使用时请注意：
 1. 建议使用反向websocket通信；
 2. nonebot2需要安装onebot适配器，并使用12版本；
 3. 需要安装插件补丁，注册拓展事件（还没写完）；
