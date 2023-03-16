import { defineUserConfig } from 'vuepress'
import { hopeTheme } from "vuepress-theme-hope"
import { searchProPlugin } from "vuepress-plugin-search-pro"

export default defineUserConfig({
  lang: 'zh-CN',
  base: '/ComWeChatBotClient/',
  title: 'ComWeChat Client',
  head: [['link', { rel: 'icon', href: '/image/logo.png' }]],
  description: '基于ComWeCahtRobot的微信协议端，支持onebot12',
  theme: hopeTheme({
    // url
    hostname: 'http://localhost:8080/ComWeChatBotClient',
    // logo
    favicon: '/image/logo.png',
    // repo
    repo: 'JustUndertaker/ComWeChatBotClient',
    // 热更新，debug用
    hotReload: true,
    // 编辑功能
    editLink: false,
    // 纯净版
    pure: true,
    // 显示页脚
    displayFooter: true,
    // 页脚
    footer: "MIT LICENSE | Copyright © <a href='https://github.com/JustUndertaker'>JustUndertaker</a>",
    // 侧边栏
    sidebar: [
      {
        text: '开始',
        link: '/guide/',
      },
      {
        text: '消息段',
        link: '/message/',
      },
      {
        text: '事件',
        collapsible: true,
        link: '/event/meta.md',
        children: [
          '/event/meta.md',
          '/event/message.md',
          '/event/request.md',
          '/event/notice.md',
        ],
      },
      {
        text: '动作',
        collapsible: true,
        link: '/action/meta.md',
        children: [
          '/action/meta.md',
          '/action/private.md',
          '/action/group.md',
          '/action/file.md',
        ]
      }
    ]
  }),
  plugins: [
    searchProPlugin({
      // 索引全部内容
      indexContent: true,
    })
  ],
})

