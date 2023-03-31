import { defineUserConfig } from 'vuepress';
import { hopeTheme } from "vuepress-theme-hope";
import { searchProPlugin } from "vuepress-plugin-search-pro";
import { shikiPlugin } from "@vuepress/plugin-shiki";

export default defineUserConfig({
  lang: 'zh-CN',
  base: '/ComWeChatBotClient/',
  title: 'ComWeChat Client',
  markdown: {
    code: {
      lineNumbers: false,
    }
  },
  head: [['link', { rel: 'icon', href: '/image/logo.png' }]],
  description: '基于ComWeCahtRobot的微信协议端，支持onebot12',
  theme: hopeTheme({
    // url
    hostname: 'https://justundertaker.github.io/ComWeChatBotClient/',
    // 站点图标
    favicon: '/image/logo.png',
    // logo
    logo: '/image/logo.png',
    // 打印
    print: false,
    // repo
    repo: 'JustUndertaker/ComWeChatBotClient',
    // 热更新，debug用
    hotReload: false,
    // 编辑功能
    editLink: false,
    // 纯净版
    pure: true,
    // 图标资源
    iconAssets: 'iconify',
    // 显示页脚
    displayFooter: true,
    // 页脚
    footer: "AGPL-3.0 LICENSE | Copyright © <a href='https://github.com/JustUndertaker'>JustUndertaker</a>",
    // 侧边栏
    sidebar: [
      {
        text: '开始',
        icon: 'icons8:idea',
        link: '/guide/',
      },
      {
        text: '消息段',
        icon: 'mdi:message-processing-outline',
        link: '/message/',
      },
      {
        text: '事件',
        icon: 'mdi:event-clock',
        collapsible: true,
        link: '/event/meta.md',
        children: [{
          text: '元事件',
          icon: 'ph:meta-logo',
          link: '/event/meta.md',
        },
        {
          text: '消息事件',
          icon: 'mdi:message-processing-outline',
          link: '/event/message.md',
        },
        {
          text: '请求事件',
          icon: 'ph:git-pull-request',
          link: '/event/request.md',
        },
        {
          text: '通知事件',
          icon: 'fe:notice-active',
          link: '/event/notice.md',
        }
        ],
      },
      {
        text: '动作',
        icon: 'material-symbols:call-to-action-outline',
        collapsible: true,
        link: '/action/meta.md',
        children: [
          {
            text: '元动作',
            icon: 'ph:meta-logo',
            link: '/action/meta.md',
          },
          {
            text: '消息动作',
            icon: 'mdi:message-processing-outline',
            link: '/action/message.md'
          },
          {
            text: '个人动作',
            icon: 'fluent:inprivate-account-16-filled',
            link: '/action/private.md',
          },
          {
            text: '群组动作',
            icon: 'material-symbols:group',
            link: '/action/group.md',
          },
          {
            text: '文件动作',
            icon: 'ic:outline-insert-drive-file',
            link: '/action/file.md'
          },
          {
            text: '拓展动作',
            icon: 'fluent:extension-16-filled',
            link: '/action/expand.md',
          }
        ]
      }
    ],
    plugins: {
      // md插件
      mdEnhance: {
        tasklist: true,
        tabs: true,
      },
      // 默认代码高亮
      prismjs: false,
    }
  }),
  plugins: [
    // 搜索插件
    searchProPlugin({
      // 索引全部内容
      indexContent: true,
    }),
    // shiki代码高亮
    shikiPlugin({
      theme: "one-dark-pro",
    })
  ],
})

