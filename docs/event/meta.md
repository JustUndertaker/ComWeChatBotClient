# 元事件
::: tip Onebot12
元事件是 OneBot 实现内部自发产生的一类事件，例如心跳等，与 OneBot 本身的运行状态有关，与实现对应的机器人平台无关。
:::
本项目实现了以下的元事件。
## `connect` 连接
对于正向 WebSocket 和反向 WebSocket 通信方式，OneBot 实现应在连接建立后立即产生一个连接事件，以向应用端推送当前实现端的相关版本信息。连接事件必须是一次成功的正向或反向 WebSocket 连接上传输的第一个事件。

HTTP 和 HTTP Webhook 通信方式不需要产生连接事件。
## `heartbeat` 心跳
当 enabled 配置为 true 时，OneBot 实现应该每隔 interval 产生一个心跳事件。
## `status_update` 状态更新
对于正向 WebSocket 和反向 WebSocket 通信方式，OneBot 实现应在连接建立后的适当时机（如所有机器人账号登录完成后）产生一个状态更新事件，发送所有机器人账号的状态。

对于 HTTP Webhook 通信方式，OneBot 实现应在启动后的适当时机（如所有机器人账号登录完成后）产生一个状态更新事件，发送所有机器人账号的状态。

在上述时机首次产生事件后，实现应在机器人账号或实现本身状态有变化时产生状态更新事件。
