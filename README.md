![ComWeChatBotClient](https://socialify.git.ci/JustUndertaker/ComWeChatBotClient/image?description=1&font=Inter&name=1&pattern=Circuit%20Board&theme=Auto)
<p align="center">
    <a href="https://onebot.dev/"><img src="https://img.shields.io/badge/OneBot-12-black?logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAHAAAABwCAMAAADxPgR5AAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFnZVJlYWR5ccllPAAAAAxQTFRF////29vbr6+vAAAAk1hCcwAAAAR0Uk5T////AEAqqfQAAAKcSURBVHja7NrbctswDATQXfD//zlpO7FlmwAWIOnOtNaTM5JwDMa8E+PNFz7g3waJ24fviyDPgfhz8fHP39cBcBL9KoJbQUxjA2iYqHL3FAnvzhL4GtVNUcoSZe6eSHizBcK5LL7dBr2AUZlev1ARRHCljzRALIEog6H3U6bCIyqIZdAT0eBuJYaGiJaHSjmkYIZd+qSGWAQnIaz2OArVnX6vrItQvbhZJtVGB5qX9wKqCMkb9W7aexfCO/rwQRBzsDIsYx4AOz0nhAtWu7bqkEQBO0Pr+Ftjt5fFCUEbm0Sbgdu8WSgJ5NgH2iu46R/o1UcBXJsFusWF/QUaz3RwJMEgngfaGGdSxJkE/Yg4lOBryBiMwvAhZrVMUUvwqU7F05b5WLaUIN4M4hRocQQRnEedgsn7TZB3UCpRrIJwQfqvGwsg18EnI2uSVNC8t+0QmMXogvbPg/xk+Mnw/6kW/rraUlvqgmFreAA09xW5t0AFlHrQZ3CsgvZm0FbHNKyBmheBKIF2cCA8A600aHPmFtRB1XvMsJAiza7LpPog0UJwccKdzw8rdf8MyN2ePYF896LC5hTzdZqxb6VNXInaupARLDNBWgI8spq4T0Qb5H4vWfPmHo8OyB1ito+AysNNz0oglj1U955sjUN9d41LnrX2D/u7eRwxyOaOpfyevCWbTgDEoilsOnu7zsKhjRCsnD/QzhdkYLBLXjiK4f3UWmcx2M7PO21CKVTH84638NTplt6JIQH0ZwCNuiWAfvuLhdrcOYPVO9eW3A67l7hZtgaY9GZo9AFc6cryjoeFBIWeU+npnk/nLE0OxCHL1eQsc1IciehjpJv5mqCsjeopaH6r15/MrxNnVhu7tmcslay2gO2Z1QfcfX0JMACG41/u0RrI9QAAAABJRU5ErkJggg==" alt="onebot12"></a>
    <a href="https://github.com/JustUndertaker/ComWeChatBotClient/blob/main/LICENSE"><img src="https://img.shields.io/github/license/JustUndertaker/ComWeChatBotClient" alt="License"></a>
    <a href="https://github.com/JustUndertaker/ComWeChatBotClient/releases"><img src="https://img.shields.io/github/v/release/JustUndertaker/ComWeChatBotClient?color=blueviolet&include_prereleases" alt="release"></a>
</p>

## 简介

`ComWeChatRobot`的客户端封装，支持`onebot12`通信协议。

## 许可证
`ComWeChatRobot Client` 采用 [AGPLv3](https://github.com/JustUndertaker/ComWeChatBotClient/blob/main/LICENSE) 协议开源，不鼓励、不支持一切商业使用。

## 上游依赖

- [ComWeChatRobot](https://github.com/ljc545w/ComWeChatRobot)：PC微信机器人，实现获取通讯录，发送文本、图片、文件等消息，封装COM接口供Python、C#调用

## 支持的微信版本

- **3.7.0.30**: 下载连接在 [这里](https://github.com/tom-snow/wechat-windows-versions/releases/download/v3.7.0.30/WeChatSetup-3.7.0.30.exe)

## 文档

文档连接：[传送门](https://justundertaker.github.io/ComWeChatBotClient/)

## Onebot12支持

- [x] HTTP
- [x] HTTP Webhook
- [x] 正向 Websocket
- [x] 反向 Websocket

## 更新日志
### 2023/6/5 V0.0.8
 - 修复status_update元事件缺失
 - 发送消息遇到错误不会直接返回failed，而是尝试将所有消息段发出
 - 处理其他程序分享的app消息
### 2023/4/16 v0.0.7
 - 修复需要两次ctrl+c才能退出的问题
 - 修复备份数据库接口
### 2023/4/8 v0.0.6
 - 修复`反向 Websocket` 子协议问题
 - `Webhook` 和 `反向 Websocket` 支持多地址
### 2023/4/6 v0.0.5
 - 修复定时器模块启动
### 2023/4/4 v0.0.4
 - 修复定时模块启动问题
 - 限制请求action日志的长度
 - 添加自动清理文件缓存任务
### 2023/4/2 v0.0.3
 - 修复ws buffer缓冲区大小问题。
 - 重写file manager保存文件的命名逻辑
 - 修复部分bug
### 2023/4/1 v0.0.2
 - 修复群聊发送不了纯文本消息的bug。
 - 修改部分文档。
### 2023/3/29 v0.0.1
- 初步可用，写个文档应该不会被发现吧。

### 2023/3/16

-  随便写写啦，反正不会写。
