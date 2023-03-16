import { defineUserConfig } from 'vuepress'
import { defaultTheme } from '@vuepress/theme-default'

export default defineUserConfig({
  lang: 'zh-CN',
  base: '/ComWeChatBotClient/',
  title: 'ComWeChat Client',
  head: [['link', { rel: 'icon', href: '/image/logo.png' }]],
  description: '基于ComWeCahtRobot的微信协议端，支持onebot12',
  theme: defaultTheme({
    // logo
    logo: '/image/logo.png',
    // repo
    repo: 'JustUndertaker/ComWeChatBotClient',
    editLink: false,
    // 导航栏
    navbar: [
      {
        text: '导航',
        link: `/guide/`,
        activeMatch: '^/guide',
      },
      {
        text: '消息段',
        link: '/message/',
        activeMatch: '^/message',
      },
      {
        text: '事件',
        children: [
          {
            text: '元事件',
            link: '/event/meta.md',
          },
          {
            text: '消息事件',
            link: '/event/message.md',
          },
          {
            text: '请求事件',
            link: '/event/request.md',
          },
          {
            text: '通知事件',
            link: '/event/notice.md',
          },
        ],
      },
      {
        text: '动作',
        children: [
          {
            text: '元动作',
            link: '/action/meta.md',
          },
          {
            text: '个人动作',
            link: '/action/private.md',
          },
          {
            text: '群动作',
            link: '/action/group.md',
          },
          {
            text: '文件动作',
            link: '/action/file.md',
          }
        ]
      }
    ],
    // 侧边栏
    sidebar: {
      '/guide/': [{
        text: '导航',
        link: '/guide/',
      }],
      '/message/': [{
        text: '消息段',
        link: '/message/',
      }],
      '/event/': [{
        text: '事件',
        link: '/event/meta.md',
        children: [
          '/event/meta.md',
          '/event/message.md',
          '/event/request.md',
          '/event/notice.md',
        ],
      }
      ],
      '/action/': [
        {
          text: '动作',
          link: '/action/meta.md',
          children: [
            '/action/meta.md',
            '/action/private.md',
            '/action/group.md',
            '/action/file.md',
          ]
        }

      ]
    },
    tip: '说明',
    warning: '注意',
    danger: '非常注意！',
  }),
})

