import{_ as r,W as y,X as i,Y as s,Z as l,$ as a,a0 as n,D as p}from"./framework-a17ef302.js";const A={},F=s("h1",{id:"元动作",tabindex:"-1"},[s("a",{class:"header-anchor",href:"#元动作","aria-hidden":"true"},"#"),l(" 元动作")],-1),d=s("div",{class:"hint-container tip"},[s("p",{class:"hint-container-title"},"Onebot12"),s("p",null,"元动作是用于对 OneBot 实现进行控制、检查等的动作，例如获取版本信息等，仅与 OneBot 本身交互，与实现对应的机器人平台无关。")],-1),_={id:"获取最新事件列表",tabindex:"-1"},C=s("a",{class:"header-anchor",href:"#获取最新事件列表","aria-hidden":"true"},"#",-1),u=s("p",null,[l("action: "),s("code",null,"get_latest_events")],-1),g=s("p",null,"仅 HTTP 通信方式支持，用于轮询获取事件。",-1),b=s("table",null,[s("thead",null,[s("tr",null,[s("th",{style:{"text-align":"center"}},"字段名"),s("th",{style:{"text-align":"center"}},"数据类型"),s("th",{style:{"text-align":"center"}},"默认值"),s("th",{style:{"text-align":"center"}},"说明")])]),s("tbody",null,[s("tr",null,[s("td",{style:{"text-align":"center"}},[s("code",null,"limit")]),s("td",{style:{"text-align":"center"}},"int64"),s("td",{style:{"text-align":"center"}},"0"),s("td",{style:{"text-align":"center"}},"获取的事件数量上限，0 表示不限制")]),s("tr",null,[s("td",{style:{"text-align":"center"}},[s("code",null,"timeout")]),s("td",{style:{"text-align":"center"}},"int64"),s("td",{style:{"text-align":"center"}},"0"),s("td",{style:{"text-align":"center"}},"没有事件时最多等待的秒数，0 表示使用短轮询，不等待")])])],-1),h=s("p",null,"除元事件外的事件列表，从旧到新排序。",-1),x=s("div",{class:"language-json","data-ext":"json"},[s("pre",{class:"shiki one-dark-pro",style:{"background-color":"#282c34"},tabindex:"0"},[s("code",null,[s("span",{class:"line"},[s("span",{style:{color:"#ABB2BF"}},"{")]),l(`
`),s("span",{class:"line"},[s("span",{style:{color:"#ABB2BF"}},"    "),s("span",{style:{color:"#E06C75"}},'"action"'),s("span",{style:{color:"#ABB2BF"}},": "),s("span",{style:{color:"#98C379"}},'"get_latest_events"'),s("span",{style:{color:"#ABB2BF"}},",")]),l(`
`),s("span",{class:"line"},[s("span",{style:{color:"#ABB2BF"}},"    "),s("span",{style:{color:"#E06C75"}},'"params"'),s("span",{style:{color:"#ABB2BF"}},": {")]),l(`
`),s("span",{class:"line"},[s("span",{style:{color:"#ABB2BF"}},"        "),s("span",{style:{color:"#E06C75"}},'"limit"'),s("span",{style:{color:"#ABB2BF"}},": "),s("span",{style:{color:"#D19A66"}},"100"),s("span",{style:{color:"#ABB2BF"}},",")]),l(`
`),s("span",{class:"line"},[s("span",{style:{color:"#ABB2BF"}},"        "),s("span",{style:{color:"#E06C75"}},'"timeout"'),s("span",{style:{color:"#ABB2BF"}},": "),s("span",{style:{color:"#D19A66"}},"0")]),l(`
`),s("span",{class:"line"},[s("span",{style:{color:"#ABB2BF"}},"    }")]),l(`
`),s("span",{class:"line"},[s("span",{style:{color:"#ABB2BF"}},"}")]),l(`
`),s("span",{class:"line"})])])],-1),v=s("div",{class:"language-json","data-ext":"json"},[s("pre",{class:"shiki one-dark-pro",style:{"background-color":"#282c34"},tabindex:"0"},[s("code",null,[s("span",{class:"line"},[s("span",{style:{color:"#ABB2BF"}},"{")]),l(`
`),s("span",{class:"line"},[s("span",{style:{color:"#ABB2BF"}},"    "),s("span",{style:{color:"#E06C75"}},'"status"'),s("span",{style:{color:"#ABB2BF"}},": "),s("span",{style:{color:"#98C379"}},'"ok"'),s("span",{style:{color:"#ABB2BF"}},",")]),l(`
`),s("span",{class:"line"},[s("span",{style:{color:"#ABB2BF"}},"    "),s("span",{style:{color:"#E06C75"}},'"retcode"'),s("span",{style:{color:"#ABB2BF"}},": "),s("span",{style:{color:"#D19A66"}},"0"),s("span",{style:{color:"#ABB2BF"}},",")]),l(`
`),s("span",{class:"line"},[s("span",{style:{color:"#ABB2BF"}},"    "),s("span",{style:{color:"#E06C75"}},'"data"'),s("span",{style:{color:"#ABB2BF"}},": [")]),l(`
`),s("span",{class:"line"},[s("span",{style:{color:"#ABB2BF"}},"        {")]),l(`
`),s("span",{class:"line"},[s("span",{style:{color:"#ABB2BF"}},"            "),s("span",{style:{color:"#E06C75"}},'"id"'),s("span",{style:{color:"#ABB2BF"}},": "),s("span",{style:{color:"#98C379"}},'"b6e65187-5ac0-489c-b431-53078e9d2bbb"'),s("span",{style:{color:"#ABB2BF"}},",")]),l(`
`),s("span",{class:"line"},[s("span",{style:{color:"#ABB2BF"}},"            "),s("span",{style:{color:"#E06C75"}},'"self"'),s("span",{style:{color:"#ABB2BF"}},": {")]),l(`
`),s("span",{class:"line"},[s("span",{style:{color:"#ABB2BF"}},"                "),s("span",{style:{color:"#E06C75"}},'"platform"'),s("span",{style:{color:"#ABB2BF"}},": "),s("span",{style:{color:"#98C379"}},'"wechat"'),s("span",{style:{color:"#ABB2BF"}},",")]),l(`
`),s("span",{class:"line"},[s("span",{style:{color:"#ABB2BF"}},"                "),s("span",{style:{color:"#E06C75"}},'"user_id"'),s("span",{style:{color:"#ABB2BF"}},": "),s("span",{style:{color:"#98C379"}},'"123234"')]),l(`
`),s("span",{class:"line"},[s("span",{style:{color:"#ABB2BF"}},"            },")]),l(`
`),s("span",{class:"line"},[s("span",{style:{color:"#ABB2BF"}},"            "),s("span",{style:{color:"#E06C75"}},'"time"'),s("span",{style:{color:"#ABB2BF"}},": "),s("span",{style:{color:"#D19A66"}},"1632847927.599013"),s("span",{style:{color:"#ABB2BF"}},",")]),l(`
`),s("span",{class:"line"},[s("span",{style:{color:"#ABB2BF"}},"            "),s("span",{style:{color:"#E06C75"}},'"type"'),s("span",{style:{color:"#ABB2BF"}},": "),s("span",{style:{color:"#98C379"}},'"message"'),s("span",{style:{color:"#ABB2BF"}},",")]),l(`
`),s("span",{class:"line"},[s("span",{style:{color:"#ABB2BF"}},"            "),s("span",{style:{color:"#E06C75"}},'"detail_type"'),s("span",{style:{color:"#ABB2BF"}},": "),s("span",{style:{color:"#98C379"}},'"private"'),s("span",{style:{color:"#ABB2BF"}},",")]),l(`
`),s("span",{class:"line"},[s("span",{style:{color:"#ABB2BF"}},"            "),s("span",{style:{color:"#E06C75"}},'"sub_type"'),s("span",{style:{color:"#ABB2BF"}},": "),s("span",{style:{color:"#98C379"}},'""'),s("span",{style:{color:"#ABB2BF"}},",")]),l(`
`),s("span",{class:"line"},[s("span",{style:{color:"#ABB2BF"}},"            "),s("span",{style:{color:"#E06C75"}},'"message_id"'),s("span",{style:{color:"#ABB2BF"}},": "),s("span",{style:{color:"#98C379"}},'"6283"'),s("span",{style:{color:"#ABB2BF"}},",")]),l(`
`),s("span",{class:"line"},[s("span",{style:{color:"#ABB2BF"}},"            "),s("span",{style:{color:"#E06C75"}},'"message"'),s("span",{style:{color:"#ABB2BF"}},": [")]),l(`
`),s("span",{class:"line"},[s("span",{style:{color:"#ABB2BF"}},"                {")]),l(`
`),s("span",{class:"line"},[s("span",{style:{color:"#ABB2BF"}},"                    "),s("span",{style:{color:"#E06C75"}},'"type"'),s("span",{style:{color:"#ABB2BF"}},": "),s("span",{style:{color:"#98C379"}},'"text"'),s("span",{style:{color:"#ABB2BF"}},",")]),l(`
`),s("span",{class:"line"},[s("span",{style:{color:"#ABB2BF"}},"                    "),s("span",{style:{color:"#E06C75"}},'"data"'),s("span",{style:{color:"#ABB2BF"}},": {")]),l(`
`),s("span",{class:"line"},[s("span",{style:{color:"#ABB2BF"}},"                        "),s("span",{style:{color:"#E06C75"}},'"text"'),s("span",{style:{color:"#ABB2BF"}},": "),s("span",{style:{color:"#98C379"}},'"OneBot is not a bot"')]),l(`
`),s("span",{class:"line"},[s("span",{style:{color:"#ABB2BF"}},"                    }")]),l(`
`),s("span",{class:"line"},[s("span",{style:{color:"#ABB2BF"}},"                },")]),l(`
`),s("span",{class:"line"},[s("span",{style:{color:"#ABB2BF"}},"                {")]),l(`
`),s("span",{class:"line"},[s("span",{style:{color:"#ABB2BF"}},"                    "),s("span",{style:{color:"#E06C75"}},'"type"'),s("span",{style:{color:"#ABB2BF"}},": "),s("span",{style:{color:"#98C379"}},'"image"'),s("span",{style:{color:"#ABB2BF"}},",")]),l(`
`),s("span",{class:"line"},[s("span",{style:{color:"#ABB2BF"}},"                    "),s("span",{style:{color:"#E06C75"}},'"data"'),s("span",{style:{color:"#ABB2BF"}},": {")]),l(`
`),s("span",{class:"line"},[s("span",{style:{color:"#ABB2BF"}},"                        "),s("span",{style:{color:"#E06C75"}},'"file_id"'),s("span",{style:{color:"#ABB2BF"}},": "),s("span",{style:{color:"#98C379"}},'"e30f9684-3d54-4f65-b2da-db291a477f16"')]),l(`
`),s("span",{class:"line"},[s("span",{style:{color:"#ABB2BF"}},"                    }")]),l(`
`),s("span",{class:"line"},[s("span",{style:{color:"#ABB2BF"}},"                }")]),l(`
`),s("span",{class:"line"},[s("span",{style:{color:"#ABB2BF"}},"            ],")]),l(`
`),s("span",{class:"line"},[s("span",{style:{color:"#ABB2BF"}},"            "),s("span",{style:{color:"#E06C75"}},'"alt_message"'),s("span",{style:{color:"#ABB2BF"}},": "),s("span",{style:{color:"#98C379"}},'"OneBot is not a bot[图片]"'),s("span",{style:{color:"#ABB2BF"}},",")]),l(`
`),s("span",{class:"line"},[s("span",{style:{color:"#ABB2BF"}},"            "),s("span",{style:{color:"#E06C75"}},'"user_id"'),s("span",{style:{color:"#ABB2BF"}},": "),s("span",{style:{color:"#98C379"}},'"123456788"')]),l(`
`),s("span",{class:"line"},[s("span",{style:{color:"#ABB2BF"}},"        },")]),l(`
`),s("span",{class:"line"},[s("span",{style:{color:"#ABB2BF"}},"        {")]),l(`
`),s("span",{class:"line"},[s("span",{style:{color:"#ABB2BF"}},"            "),s("span",{style:{color:"#E06C75"}},'"id"'),s("span",{style:{color:"#ABB2BF"}},": "),s("span",{style:{color:"#98C379"}},'"b6e65187-5ac0-489c-b431-53078e9d2bbb"'),s("span",{style:{color:"#ABB2BF"}},",")]),l(`
`),s("span",{class:"line"},[s("span",{style:{color:"#ABB2BF"}},"            "),s("span",{style:{color:"#E06C75"}},'"self"'),s("span",{style:{color:"#ABB2BF"}},": {")]),l(`
`),s("span",{class:"line"},[s("span",{style:{color:"#ABB2BF"}},"                "),s("span",{style:{color:"#E06C75"}},'"platform"'),s("span",{style:{color:"#ABB2BF"}},": "),s("span",{style:{color:"#98C379"}},'"qq"'),s("span",{style:{color:"#ABB2BF"}},",")]),l(`
`),s("span",{class:"line"},[s("span",{style:{color:"#ABB2BF"}},"                "),s("span",{style:{color:"#E06C75"}},'"user_id"'),s("span",{style:{color:"#ABB2BF"}},": "),s("span",{style:{color:"#98C379"}},'"123234"')]),l(`
`),s("span",{class:"line"},[s("span",{style:{color:"#ABB2BF"}},"            },")]),l(`
`),s("span",{class:"line"},[s("span",{style:{color:"#ABB2BF"}},"            "),s("span",{style:{color:"#E06C75"}},'"time"'),s("span",{style:{color:"#ABB2BF"}},": "),s("span",{style:{color:"#D19A66"}},"1632847927.599013"),s("span",{style:{color:"#ABB2BF"}},",")]),l(`
`),s("span",{class:"line"},[s("span",{style:{color:"#ABB2BF"}},"            "),s("span",{style:{color:"#E06C75"}},'"type"'),s("span",{style:{color:"#ABB2BF"}},": "),s("span",{style:{color:"#98C379"}},'"notice"'),s("span",{style:{color:"#ABB2BF"}},",")]),l(`
`),s("span",{class:"line"},[s("span",{style:{color:"#ABB2BF"}},"            "),s("span",{style:{color:"#E06C75"}},'"detail_type"'),s("span",{style:{color:"#ABB2BF"}},": "),s("span",{style:{color:"#98C379"}},'"group_member_increase"'),s("span",{style:{color:"#ABB2BF"}},",")]),l(`
`),s("span",{class:"line"},[s("span",{style:{color:"#ABB2BF"}},"            "),s("span",{style:{color:"#E06C75"}},'"sub_type"'),s("span",{style:{color:"#ABB2BF"}},": "),s("span",{style:{color:"#98C379"}},'"join"'),s("span",{style:{color:"#ABB2BF"}},",")]),l(`
`),s("span",{class:"line"},[s("span",{style:{color:"#ABB2BF"}},"            "),s("span",{style:{color:"#E06C75"}},'"user_id"'),s("span",{style:{color:"#ABB2BF"}},": "),s("span",{style:{color:"#98C379"}},'"123456788"'),s("span",{style:{color:"#ABB2BF"}},",")]),l(`
`),s("span",{class:"line"},[s("span",{style:{color:"#ABB2BF"}},"            "),s("span",{style:{color:"#E06C75"}},'"group_id"'),s("span",{style:{color:"#ABB2BF"}},": "),s("span",{style:{color:"#98C379"}},'"87654321"'),s("span",{style:{color:"#ABB2BF"}},",")]),l(`
`),s("span",{class:"line"},[s("span",{style:{color:"#ABB2BF"}},"            "),s("span",{style:{color:"#E06C75"}},'"operator_id"'),s("span",{style:{color:"#ABB2BF"}},": "),s("span",{style:{color:"#98C379"}},'"1234567"')]),l(`
`),s("span",{class:"line"},[s("span",{style:{color:"#ABB2BF"}},"        }")]),l(`
`),s("span",{class:"line"},[s("span",{style:{color:"#ABB2BF"}},"    ],")]),l(`
`),s("span",{class:"line"},[s("span",{style:{color:"#ABB2BF"}},"    "),s("span",{style:{color:"#E06C75"}},'"message"'),s("span",{style:{color:"#ABB2BF"}},": "),s("span",{style:{color:"#98C379"}},'""')]),l(`
`),s("span",{class:"line"},[s("span",{style:{color:"#ABB2BF"}},"}")]),l(`
`),s("span",{class:"line"})])])],-1),m=s("div",{class:"language-python","data-ext":"py"},[s("pre",{class:"shiki one-dark-pro",style:{"background-color":"#282c34"},tabindex:"0"},[s("code",null,[s("span",{class:"line"},[s("span",{style:{color:"#C678DD","font-style":"italic"}},"from"),s("span",{style:{color:"#ABB2BF"}}," nonebot.adapters.onebot.v12 "),s("span",{style:{color:"#C678DD","font-style":"italic"}},"import"),s("span",{style:{color:"#ABB2BF"}}," Bot")]),l(`
`),s("span",{class:"line"},[s("span",{style:{color:"#C678DD","font-style":"italic"}},"from"),s("span",{style:{color:"#ABB2BF"}}," nonebot "),s("span",{style:{color:"#C678DD","font-style":"italic"}},"import"),s("span",{style:{color:"#ABB2BF"}}," get_bot")]),l(`
`),s("span",{class:"line"}),l(`
`),s("span",{class:"line"},[s("span",{style:{color:"#C678DD"}},"async"),s("span",{style:{color:"#ABB2BF"}}," "),s("span",{style:{color:"#C678DD"}},"def"),s("span",{style:{color:"#ABB2BF"}}," "),s("span",{style:{color:"#61AFEF"}},"test"),s("span",{style:{color:"#ABB2BF"}},"():")]),l(`
`),s("span",{class:"line"},[s("span",{style:{color:"#ABB2BF"}},"    bot "),s("span",{style:{color:"#56B6C2"}},"="),s("span",{style:{color:"#ABB2BF"}}," "),s("span",{style:{color:"#61AFEF"}},"get_bot"),s("span",{style:{color:"#ABB2BF"}},"()")]),l(`
`),s("span",{class:"line"},[s("span",{style:{color:"#ABB2BF"}},"    latest_events "),s("span",{style:{color:"#56B6C2"}},"="),s("span",{style:{color:"#ABB2BF"}}," "),s("span",{style:{color:"#C678DD","font-style":"italic"}},"await"),s("span",{style:{color:"#ABB2BF"}}," bot."),s("span",{style:{color:"#61AFEF"}},"get_latest_events"),s("span",{style:{color:"#ABB2BF"}},"()")]),l(`
`),s("span",{class:"line"}),l(`
`),s("span",{class:"line"})])])],-1),E={id:"获取支持的动作列表",tabindex:"-1"},f=s("a",{class:"header-anchor",href:"#获取支持的动作列表","aria-hidden":"true"},"#",-1),D=s("p",null,[l("action: "),s("code",null,"get_supported_actions")],-1),k=s("p",null,"无.",-1),w=s("p",null,[l("支持的动作名称列表，不包括 "),s("code",null,"get_latest_events"),l("。")],-1),j=s("div",{class:"language-json","data-ext":"json"},[s("pre",{class:"shiki one-dark-pro",style:{"background-color":"#282c34"},tabindex:"0"},[s("code",null,[s("span",{class:"line"},[s("span",{style:{color:"#ABB2BF"}},"{")]),l(`
`),s("span",{class:"line"},[s("span",{style:{color:"#ABB2BF"}},"    "),s("span",{style:{color:"#E06C75"}},'"action"'),s("span",{style:{color:"#ABB2BF"}},": "),s("span",{style:{color:"#98C379"}},'"get_supported_actions"'),s("span",{style:{color:"#ABB2BF"}},",")]),l(`
`),s("span",{class:"line"},[s("span",{style:{color:"#ABB2BF"}},"    "),s("span",{style:{color:"#E06C75"}},'"params"'),s("span",{style:{color:"#ABB2BF"}},": {}")]),l(`
`),s("span",{class:"line"},[s("span",{style:{color:"#ABB2BF"}},"}")]),l(`
`),s("span",{class:"line"})])])],-1),O=s("div",{class:"language-json","data-ext":"json"},[s("pre",{class:"shiki one-dark-pro",style:{"background-color":"#282c34"},tabindex:"0"},[s("code",null,[s("span",{class:"line"},[s("span",{style:{color:"#ABB2BF"}},"{")]),l(`
`),s("span",{class:"line"},[s("span",{style:{color:"#ABB2BF"}},"    "),s("span",{style:{color:"#E06C75"}},'"status"'),s("span",{style:{color:"#ABB2BF"}},": "),s("span",{style:{color:"#98C379"}},'"ok"'),s("span",{style:{color:"#ABB2BF"}},",")]),l(`
`),s("span",{class:"line"},[s("span",{style:{color:"#ABB2BF"}},"    "),s("span",{style:{color:"#E06C75"}},'"retcode"'),s("span",{style:{color:"#ABB2BF"}},": "),s("span",{style:{color:"#D19A66"}},"0"),s("span",{style:{color:"#ABB2BF"}},",")]),l(`
`),s("span",{class:"line"},[s("span",{style:{color:"#ABB2BF"}},"    "),s("span",{style:{color:"#E06C75"}},'"data"'),s("span",{style:{color:"#ABB2BF"}},": [")]),l(`
`),s("span",{class:"line"},[s("span",{style:{color:"#ABB2BF"}},"        "),s("span",{style:{color:"#98C379"}},'"get_supported_actions"'),s("span",{style:{color:"#ABB2BF"}},",")]),l(`
`),s("span",{class:"line"},[s("span",{style:{color:"#ABB2BF"}},"        "),s("span",{style:{color:"#98C379"}},'"get_status"'),s("span",{style:{color:"#ABB2BF"}},",")]),l(`
`),s("span",{class:"line"},[s("span",{style:{color:"#ABB2BF"}},"        "),s("span",{style:{color:"#98C379"}},'"get_version"'),s("span",{style:{color:"#ABB2BF"}},",")]),l(`
`),s("span",{class:"line"},[s("span",{style:{color:"#ABB2BF"}},"        "),s("span",{style:{color:"#98C379"}},'"send_message"'),s("span",{style:{color:"#ABB2BF"}},",")]),l(`
`),s("span",{class:"line"},[s("span",{style:{color:"#ABB2BF"}},"        "),s("span",{style:{color:"#98C379"}},'"get_self_info"'),s("span",{style:{color:"#ABB2BF"}},",")]),l(`
`),s("span",{class:"line"},[s("span",{style:{color:"#ABB2BF"}},"        "),s("span",{style:{color:"#98C379"}},'"get_user_info"'),s("span",{style:{color:"#ABB2BF"}},",")]),l(`
`),s("span",{class:"line"},[s("span",{style:{color:"#ABB2BF"}},"        "),s("span",{style:{color:"#98C379"}},'"get_friend_list"'),s("span",{style:{color:"#ABB2BF"}},",")]),l(`
`),s("span",{class:"line"},[s("span",{style:{color:"#ABB2BF"}},"        "),s("span",{style:{color:"#98C379"}},'"get_group_info"'),s("span",{style:{color:"#ABB2BF"}},",")]),l(`
`),s("span",{class:"line"},[s("span",{style:{color:"#ABB2BF"}},"        "),s("span",{style:{color:"#98C379"}},'"get_group_list"'),s("span",{style:{color:"#ABB2BF"}},",")]),l(`
`),s("span",{class:"line"},[s("span",{style:{color:"#ABB2BF"}},"        "),s("span",{style:{color:"#98C379"}},'"get_group_member_info"'),s("span",{style:{color:"#ABB2BF"}},",")]),l(`
`),s("span",{class:"line"},[s("span",{style:{color:"#ABB2BF"}},"        "),s("span",{style:{color:"#98C379"}},'"get_group_member_list"'),s("span",{style:{color:"#ABB2BF"}},",")]),l(`
`),s("span",{class:"line"},[s("span",{style:{color:"#ABB2BF"}},"        "),s("span",{style:{color:"#98C379"}},'"set_group_name"'),s("span",{style:{color:"#ABB2BF"}},",")]),l(`
`),s("span",{class:"line"},[s("span",{style:{color:"#ABB2BF"}},"        "),s("span",{style:{color:"#98C379"}},'"upload_file"'),s("span",{style:{color:"#ABB2BF"}},",")]),l(`
`),s("span",{class:"line"},[s("span",{style:{color:"#ABB2BF"}},"        "),s("span",{style:{color:"#98C379"}},'"get_file"'),s("span",{style:{color:"#ABB2BF"}},",")]),l(`
`),s("span",{class:"line"},[s("span",{style:{color:"#ABB2BF"}},"        "),s("span",{style:{color:"#98C379"}},'"wx.get_public_account_list"'),s("span",{style:{color:"#ABB2BF"}},",")]),l(`
`),s("span",{class:"line"},[s("span",{style:{color:"#ABB2BF"}},"        "),s("span",{style:{color:"#98C379"}},'"wx.follow_public_number"'),s("span",{style:{color:"#ABB2BF"}},",")]),l(`
`),s("span",{class:"line"},[s("span",{style:{color:"#ABB2BF"}},"        "),s("span",{style:{color:"#98C379"}},'"wx.search_friend_by_remark"'),s("span",{style:{color:"#ABB2BF"}},",")]),l(`
`),s("span",{class:"line"},[s("span",{style:{color:"#ABB2BF"}},"        "),s("span",{style:{color:"#98C379"}},'"wx.search_friend_by_wxnumber"'),s("span",{style:{color:"#ABB2BF"}},",")]),l(`
`),s("span",{class:"line"},[s("span",{style:{color:"#ABB2BF"}},"        "),s("span",{style:{color:"#98C379"}},'"wx.search_friend_by_nickname"'),s("span",{style:{color:"#ABB2BF"}},",")]),l(`
`),s("span",{class:"line"},[s("span",{style:{color:"#ABB2BF"}},"        "),s("span",{style:{color:"#98C379"}},'"wx.check_friend_status"'),s("span",{style:{color:"#ABB2BF"}},",")]),l(`
`),s("span",{class:"line"},[s("span",{style:{color:"#ABB2BF"}},"        "),s("span",{style:{color:"#98C379"}},'"wx.get_db_handles"'),s("span",{style:{color:"#ABB2BF"}},",")]),l(`
`),s("span",{class:"line"},[s("span",{style:{color:"#ABB2BF"}},"        "),s("span",{style:{color:"#98C379"}},'"wx.execute_sql"'),s("span",{style:{color:"#ABB2BF"}},",")]),l(`
`),s("span",{class:"line"},[s("span",{style:{color:"#ABB2BF"}},"        "),s("span",{style:{color:"#98C379"}},'"wx.backup_db"'),s("span",{style:{color:"#ABB2BF"}},",")]),l(`
`),s("span",{class:"line"},[s("span",{style:{color:"#ABB2BF"}},"        "),s("span",{style:{color:"#98C379"}},'"wx.verify_friend_apply"'),s("span",{style:{color:"#ABB2BF"}},",")]),l(`
`),s("span",{class:"line"},[s("span",{style:{color:"#ABB2BF"}},"        "),s("span",{style:{color:"#98C379"}},'"wx.get_wechat_version"'),s("span",{style:{color:"#ABB2BF"}},",")]),l(`
`),s("span",{class:"line"},[s("span",{style:{color:"#ABB2BF"}},"        "),s("span",{style:{color:"#98C379"}},'"wx.change_wechat_version"'),s("span",{style:{color:"#ABB2BF"}},",")]),l(`
`),s("span",{class:"line"},[s("span",{style:{color:"#ABB2BF"}},"        "),s("span",{style:{color:"#98C379"}},'"wx.delete_friend"'),s("span",{style:{color:"#ABB2BF"}},",")]),l(`
`),s("span",{class:"line"},[s("span",{style:{color:"#ABB2BF"}},"        "),s("span",{style:{color:"#98C379"}},'"wx.edit_remark"'),s("span",{style:{color:"#ABB2BF"}},",")]),l(`
`),s("span",{class:"line"},[s("span",{style:{color:"#ABB2BF"}},"        "),s("span",{style:{color:"#98C379"}},'"wx.set_group_announcement"'),s("span",{style:{color:"#ABB2BF"}},",")]),l(`
`),s("span",{class:"line"},[s("span",{style:{color:"#ABB2BF"}},"        "),s("span",{style:{color:"#98C379"}},'"wx.set_group_nickname"'),s("span",{style:{color:"#ABB2BF"}},",")]),l(`
`),s("span",{class:"line"},[s("span",{style:{color:"#ABB2BF"}},"        "),s("span",{style:{color:"#98C379"}},'"wx.get_groupmember_nickname"'),s("span",{style:{color:"#ABB2BF"}},",")]),l(`
`),s("span",{class:"line"},[s("span",{style:{color:"#ABB2BF"}},"        "),s("span",{style:{color:"#98C379"}},'"wx.kick_groupmember"'),s("span",{style:{color:"#ABB2BF"}},",")]),l(`
`),s("span",{class:"line"},[s("span",{style:{color:"#ABB2BF"}},"        "),s("span",{style:{color:"#98C379"}},'"wx.invite_groupmember"'),s("span",{style:{color:"#ABB2BF"}},",")]),l(`
`),s("span",{class:"line"},[s("span",{style:{color:"#ABB2BF"}},"        "),s("span",{style:{color:"#98C379"}},'"wx.get_history_public_msg"'),s("span",{style:{color:"#ABB2BF"}},",")]),l(`
`),s("span",{class:"line"},[s("span",{style:{color:"#ABB2BF"}},"        "),s("span",{style:{color:"#98C379"}},'"wx.send_forward_msg"'),s("span",{style:{color:"#ABB2BF"}},",")]),l(`
`),s("span",{class:"line"},[s("span",{style:{color:"#ABB2BF"}},"        "),s("span",{style:{color:"#98C379"}},'"wx.send_xml"'),s("span",{style:{color:"#ABB2BF"}},",")]),l(`
`),s("span",{class:"line"},[s("span",{style:{color:"#ABB2BF"}},"        "),s("span",{style:{color:"#98C379"}},'"wx.send_card"'),s("span",{style:{color:"#ABB2BF"}},",")]),l(`
`),s("span",{class:"line"},[s("span",{style:{color:"#ABB2BF"}},"        "),s("span",{style:{color:"#98C379"}},'"wx.clean_file_cache"')]),l(`
`),s("span",{class:"line"},[s("span",{style:{color:"#ABB2BF"}},"    ],")]),l(`
`),s("span",{class:"line"},[s("span",{style:{color:"#ABB2BF"}},"    "),s("span",{style:{color:"#E06C75"}},'"message"'),s("span",{style:{color:"#ABB2BF"}},": "),s("span",{style:{color:"#98C379"}},'""')]),l(`
`),s("span",{class:"line"},[s("span",{style:{color:"#ABB2BF"}},"}")]),l(`
`),s("span",{class:"line"})])])],-1),T=s("div",{class:"language-python","data-ext":"py"},[s("pre",{class:"shiki one-dark-pro",style:{"background-color":"#282c34"},tabindex:"0"},[s("code",null,[s("span",{class:"line"},[s("span",{style:{color:"#C678DD","font-style":"italic"}},"from"),s("span",{style:{color:"#ABB2BF"}}," nonebot.adapters.onebot.v12 "),s("span",{style:{color:"#C678DD","font-style":"italic"}},"import"),s("span",{style:{color:"#ABB2BF"}}," Bot")]),l(`
`),s("span",{class:"line"},[s("span",{style:{color:"#C678DD","font-style":"italic"}},"from"),s("span",{style:{color:"#ABB2BF"}}," nonebot "),s("span",{style:{color:"#C678DD","font-style":"italic"}},"import"),s("span",{style:{color:"#ABB2BF"}}," get_bot")]),l(`
`),s("span",{class:"line"}),l(`
`),s("span",{class:"line"},[s("span",{style:{color:"#C678DD"}},"async"),s("span",{style:{color:"#ABB2BF"}}," "),s("span",{style:{color:"#C678DD"}},"def"),s("span",{style:{color:"#ABB2BF"}}," "),s("span",{style:{color:"#61AFEF"}},"test"),s("span",{style:{color:"#ABB2BF"}},"():")]),l(`
`),s("span",{class:"line"},[s("span",{style:{color:"#ABB2BF"}},"    bot "),s("span",{style:{color:"#56B6C2"}},"="),s("span",{style:{color:"#ABB2BF"}}," "),s("span",{style:{color:"#61AFEF"}},"get_bot"),s("span",{style:{color:"#ABB2BF"}},"()")]),l(`
`),s("span",{class:"line"},[s("span",{style:{color:"#ABB2BF"}},"    supported_actions "),s("span",{style:{color:"#56B6C2"}},"="),s("span",{style:{color:"#ABB2BF"}}," "),s("span",{style:{color:"#C678DD","font-style":"italic"}},"await"),s("span",{style:{color:"#ABB2BF"}}," bot."),s("span",{style:{color:"#61AFEF"}},"get_supported_actions"),s("span",{style:{color:"#ABB2BF"}},"()")]),l(`
`),s("span",{class:"line"}),l(`
`),s("span",{class:"line"})])])],-1),q={id:"获取运行状态",tabindex:"-1"},N=s("a",{class:"header-anchor",href:"#获取运行状态","aria-hidden":"true"},"#",-1),V=s("p",null,[l("action: "),s("code",null,"get_status")],-1),W=s("p",null,"无",-1),H=s("table",null,[s("thead",null,[s("tr",null,[s("th",{style:{"text-align":"center"}},"字段名"),s("th",{style:{"text-align":"center"}},"数据类型"),s("th",{style:{"text-align":"center"}},"说明")])]),s("tbody",null,[s("tr",null,[s("td",{style:{"text-align":"center"}},[s("code",null,"good")]),s("td",{style:{"text-align":"center"}},"bool"),s("td",{style:{"text-align":"center"}},"是否各项状态都符合预期，OneBot 实现各模块均正常")]),s("tr",null,[s("td",{style:{"text-align":"center"}},[s("code",null,"bots")]),s("td",{style:{"text-align":"center"}},"list[object]"),s("td",{style:{"text-align":"center"}},"当前 OneBot Connect 连接上所有机器人账号的状态列表")])])],-1),P=s("p",null,[l("其中，"),s("code",null,"bots"),l(" 的每一个元素具有下面这些字段：")],-1),X=s("table",null,[s("thead",null,[s("tr",null,[s("th",{style:{"text-align":"center"}},"字段名"),s("th",{style:{"text-align":"center"}},"数据类型"),s("th",{style:{"text-align":"center"}},"说明")])]),s("tbody",null,[s("tr",null,[s("td",{style:{"text-align":"center"}},"self"),s("td",{style:{"text-align":"center"}},"self"),s("td",{style:{"text-align":"center"}},"机器人自身标识")]),s("tr",null,[s("td",{style:{"text-align":"center"}},"online"),s("td",{style:{"text-align":"center"}},"bool"),s("td",{style:{"text-align":"center"}},"机器人账号是否在线（可收发消息等）")])])],-1),Y=s("div",{class:"language-json","data-ext":"json"},[s("pre",{class:"shiki one-dark-pro",style:{"background-color":"#282c34"},tabindex:"0"},[s("code",null,[s("span",{class:"line"},[s("span",{style:{color:"#ABB2BF"}},"{")]),l(`
`),s("span",{class:"line"},[s("span",{style:{color:"#ABB2BF"}},"    "),s("span",{style:{color:"#E06C75"}},'"action"'),s("span",{style:{color:"#ABB2BF"}},": "),s("span",{style:{color:"#98C379"}},'"get_status"'),s("span",{style:{color:"#ABB2BF"}},",")]),l(`
`),s("span",{class:"line"},[s("span",{style:{color:"#ABB2BF"}},"    "),s("span",{style:{color:"#E06C75"}},'"params"'),s("span",{style:{color:"#ABB2BF"}},": {}")]),l(`
`),s("span",{class:"line"},[s("span",{style:{color:"#ABB2BF"}},"}")]),l(`
`),s("span",{class:"line"})])])],-1),Z=s("div",{class:"language-json","data-ext":"json"},[s("pre",{class:"shiki one-dark-pro",style:{"background-color":"#282c34"},tabindex:"0"},[s("code",null,[s("span",{class:"line"},[s("span",{style:{color:"#ABB2BF"}},"{")]),l(`
`),s("span",{class:"line"},[s("span",{style:{color:"#ABB2BF"}},"    "),s("span",{style:{color:"#E06C75"}},'"status"'),s("span",{style:{color:"#ABB2BF"}},": "),s("span",{style:{color:"#98C379"}},'"ok"'),s("span",{style:{color:"#ABB2BF"}},",")]),l(`
`),s("span",{class:"line"},[s("span",{style:{color:"#ABB2BF"}},"    "),s("span",{style:{color:"#E06C75"}},'"retcode"'),s("span",{style:{color:"#ABB2BF"}},": "),s("span",{style:{color:"#D19A66"}},"0"),s("span",{style:{color:"#ABB2BF"}},",")]),l(`
`),s("span",{class:"line"},[s("span",{style:{color:"#ABB2BF"}},"    "),s("span",{style:{color:"#E06C75"}},'"data"'),s("span",{style:{color:"#ABB2BF"}},": {")]),l(`
`),s("span",{class:"line"},[s("span",{style:{color:"#ABB2BF"}},"        "),s("span",{style:{color:"#E06C75"}},'"good"'),s("span",{style:{color:"#ABB2BF"}},": "),s("span",{style:{color:"#D19A66"}},"true"),s("span",{style:{color:"#ABB2BF"}},",")]),l(`
`),s("span",{class:"line"},[s("span",{style:{color:"#ABB2BF"}},"        "),s("span",{style:{color:"#E06C75"}},'"bots"'),s("span",{style:{color:"#ABB2BF"}},": [")]),l(`
`),s("span",{class:"line"},[s("span",{style:{color:"#ABB2BF"}},"            {")]),l(`
`),s("span",{class:"line"},[s("span",{style:{color:"#ABB2BF"}},"                "),s("span",{style:{color:"#E06C75"}},'"self"'),s("span",{style:{color:"#ABB2BF"}},": {")]),l(`
`),s("span",{class:"line"},[s("span",{style:{color:"#ABB2BF"}},"                    "),s("span",{style:{color:"#E06C75"}},'"platform"'),s("span",{style:{color:"#ABB2BF"}},": "),s("span",{style:{color:"#98C379"}},'"wechat"'),s("span",{style:{color:"#ABB2BF"}},",")]),l(`
`),s("span",{class:"line"},[s("span",{style:{color:"#ABB2BF"}},"                    "),s("span",{style:{color:"#E06C75"}},'"user_id"'),s("span",{style:{color:"#ABB2BF"}},": "),s("span",{style:{color:"#98C379"}},'"xxxx"')]),l(`
`),s("span",{class:"line"},[s("span",{style:{color:"#ABB2BF"}},"                },")]),l(`
`),s("span",{class:"line"},[s("span",{style:{color:"#ABB2BF"}},"                "),s("span",{style:{color:"#E06C75"}},'"online"'),s("span",{style:{color:"#ABB2BF"}},": "),s("span",{style:{color:"#D19A66"}},"true")]),l(`
`),s("span",{class:"line"},[s("span",{style:{color:"#ABB2BF"}},"            }")]),l(`
`),s("span",{class:"line"},[s("span",{style:{color:"#ABB2BF"}},"        ]")]),l(`
`),s("span",{class:"line"},[s("span",{style:{color:"#ABB2BF"}},"    },")]),l(`
`),s("span",{class:"line"},[s("span",{style:{color:"#ABB2BF"}},"    "),s("span",{style:{color:"#E06C75"}},'"message"'),s("span",{style:{color:"#ABB2BF"}},": "),s("span",{style:{color:"#98C379"}},'""')]),l(`
`),s("span",{class:"line"},[s("span",{style:{color:"#ABB2BF"}},"}")]),l(`
`),s("span",{class:"line"})])])],-1),$=s("div",{class:"language-python","data-ext":"py"},[s("pre",{class:"shiki one-dark-pro",style:{"background-color":"#282c34"},tabindex:"0"},[s("code",null,[s("span",{class:"line"},[s("span",{style:{color:"#C678DD","font-style":"italic"}},"from"),s("span",{style:{color:"#ABB2BF"}}," nonebot.adapters.onebot.v12 "),s("span",{style:{color:"#C678DD","font-style":"italic"}},"import"),s("span",{style:{color:"#ABB2BF"}}," Bot")]),l(`
`),s("span",{class:"line"},[s("span",{style:{color:"#C678DD","font-style":"italic"}},"from"),s("span",{style:{color:"#ABB2BF"}}," nonebot "),s("span",{style:{color:"#C678DD","font-style":"italic"}},"import"),s("span",{style:{color:"#ABB2BF"}}," get_bot")]),l(`
`),s("span",{class:"line"}),l(`
`),s("span",{class:"line"},[s("span",{style:{color:"#C678DD"}},"async"),s("span",{style:{color:"#ABB2BF"}}," "),s("span",{style:{color:"#C678DD"}},"def"),s("span",{style:{color:"#ABB2BF"}}," "),s("span",{style:{color:"#61AFEF"}},"test"),s("span",{style:{color:"#ABB2BF"}},"():")]),l(`
`),s("span",{class:"line"},[s("span",{style:{color:"#ABB2BF"}},"    bot "),s("span",{style:{color:"#56B6C2"}},"="),s("span",{style:{color:"#ABB2BF"}}," "),s("span",{style:{color:"#61AFEF"}},"get_bot"),s("span",{style:{color:"#ABB2BF"}},"()")]),l(`
`),s("span",{class:"line"},[s("span",{style:{color:"#ABB2BF"}},"    status "),s("span",{style:{color:"#56B6C2"}},"="),s("span",{style:{color:"#ABB2BF"}}," "),s("span",{style:{color:"#C678DD","font-style":"italic"}},"await"),s("span",{style:{color:"#ABB2BF"}}," bot."),s("span",{style:{color:"#61AFEF"}},"get_status"),s("span",{style:{color:"#ABB2BF"}},"()")]),l(`
`),s("span",{class:"line"}),l(`
`),s("span",{class:"line"})])])],-1),z={id:"获取版本信息",tabindex:"-1"},G=s("a",{class:"header-anchor",href:"#获取版本信息","aria-hidden":"true"},"#",-1),I=s("p",null,[l("action: "),s("code",null,"get_version")],-1),J=s("p",null,"无",-1),K=s("table",null,[s("thead",null,[s("tr",null,[s("th",{style:{"text-align":"center"}},"字段名"),s("th",{style:{"text-align":"center"}},"数据类型"),s("th",{style:{"text-align":"center"}},"说明")])]),s("tbody",null,[s("tr",null,[s("td",{style:{"text-align":"center"}},[s("code",null,"impl")]),s("td",{style:{"text-align":"center"}},"string"),s("td",{style:{"text-align":"center"}},[l("实现名称，"),s("code",null,"ComWechat")])]),s("tr",null,[s("td",{style:{"text-align":"center"}},[s("code",null,"version")]),s("td",{style:{"text-align":"center"}},"string"),s("td",{style:{"text-align":"center"}},"版本号")]),s("tr",null,[s("td",{style:{"text-align":"center"}},[s("code",null,"onebot_version")]),s("td",{style:{"text-align":"center"}},"string"),s("td",{style:{"text-align":"center"}},"OneBot 标准版本号")])])],-1),L=s("div",{class:"language-json","data-ext":"json"},[s("pre",{class:"shiki one-dark-pro",style:{"background-color":"#282c34"},tabindex:"0"},[s("code",null,[s("span",{class:"line"},[s("span",{style:{color:"#ABB2BF"}},"{")]),l(`
`),s("span",{class:"line"},[s("span",{style:{color:"#ABB2BF"}},"    "),s("span",{style:{color:"#E06C75"}},'"action"'),s("span",{style:{color:"#ABB2BF"}},": "),s("span",{style:{color:"#98C379"}},'"get_version"'),s("span",{style:{color:"#ABB2BF"}},",")]),l(`
`),s("span",{class:"line"},[s("span",{style:{color:"#ABB2BF"}},"    "),s("span",{style:{color:"#E06C75"}},'"params"'),s("span",{style:{color:"#ABB2BF"}},": {}")]),l(`
`),s("span",{class:"line"},[s("span",{style:{color:"#ABB2BF"}},"}")]),l(`
`),s("span",{class:"line"})])])],-1),M=s("div",{class:"language-json","data-ext":"json"},[s("pre",{class:"shiki one-dark-pro",style:{"background-color":"#282c34"},tabindex:"0"},[s("code",null,[s("span",{class:"line"},[s("span",{style:{color:"#ABB2BF"}},"{")]),l(`
`),s("span",{class:"line"},[s("span",{style:{color:"#ABB2BF"}},"    "),s("span",{style:{color:"#E06C75"}},'"status"'),s("span",{style:{color:"#ABB2BF"}},": "),s("span",{style:{color:"#98C379"}},'"ok"'),s("span",{style:{color:"#ABB2BF"}},",")]),l(`
`),s("span",{class:"line"},[s("span",{style:{color:"#ABB2BF"}},"    "),s("span",{style:{color:"#E06C75"}},'"retcode"'),s("span",{style:{color:"#ABB2BF"}},": "),s("span",{style:{color:"#D19A66"}},"0"),s("span",{style:{color:"#ABB2BF"}},",")]),l(`
`),s("span",{class:"line"},[s("span",{style:{color:"#ABB2BF"}},"    "),s("span",{style:{color:"#E06C75"}},'"data"'),s("span",{style:{color:"#ABB2BF"}},": {")]),l(`
`),s("span",{class:"line"},[s("span",{style:{color:"#ABB2BF"}},"        "),s("span",{style:{color:"#E06C75"}},'"impl"'),s("span",{style:{color:"#ABB2BF"}},": "),s("span",{style:{color:"#98C379"}},'"ComWechat"'),s("span",{style:{color:"#ABB2BF"}},",")]),l(`
`),s("span",{class:"line"},[s("span",{style:{color:"#ABB2BF"}},"        "),s("span",{style:{color:"#E06C75"}},'"version"'),s("span",{style:{color:"#ABB2BF"}},": "),s("span",{style:{color:"#98C379"}},'"v1.0"'),s("span",{style:{color:"#ABB2BF"}},",")]),l(`
`),s("span",{class:"line"},[s("span",{style:{color:"#ABB2BF"}},"        "),s("span",{style:{color:"#E06C75"}},'"onebot_version"'),s("span",{style:{color:"#ABB2BF"}},": "),s("span",{style:{color:"#98C379"}},'"12"')]),l(`
`),s("span",{class:"line"},[s("span",{style:{color:"#ABB2BF"}},"    },")]),l(`
`),s("span",{class:"line"},[s("span",{style:{color:"#ABB2BF"}},"    "),s("span",{style:{color:"#E06C75"}},'"message"'),s("span",{style:{color:"#ABB2BF"}},": "),s("span",{style:{color:"#98C379"}},'""')]),l(`
`),s("span",{class:"line"},[s("span",{style:{color:"#ABB2BF"}},"}")]),l(`
`),s("span",{class:"line"})])])],-1),Q=s("div",{class:"language-python","data-ext":"py"},[s("pre",{class:"shiki one-dark-pro",style:{"background-color":"#282c34"},tabindex:"0"},[s("code",null,[s("span",{class:"line"},[s("span",{style:{color:"#C678DD","font-style":"italic"}},"from"),s("span",{style:{color:"#ABB2BF"}}," nonebot.adapters.onebot.v12 "),s("span",{style:{color:"#C678DD","font-style":"italic"}},"import"),s("span",{style:{color:"#ABB2BF"}}," Bot")]),l(`
`),s("span",{class:"line"},[s("span",{style:{color:"#C678DD","font-style":"italic"}},"from"),s("span",{style:{color:"#ABB2BF"}}," nonebot "),s("span",{style:{color:"#C678DD","font-style":"italic"}},"import"),s("span",{style:{color:"#ABB2BF"}}," get_bot")]),l(`
`),s("span",{class:"line"}),l(`
`),s("span",{class:"line"},[s("span",{style:{color:"#C678DD"}},"async"),s("span",{style:{color:"#ABB2BF"}}," "),s("span",{style:{color:"#C678DD"}},"def"),s("span",{style:{color:"#ABB2BF"}}," "),s("span",{style:{color:"#61AFEF"}},"test"),s("span",{style:{color:"#ABB2BF"}},"():")]),l(`
`),s("span",{class:"line"},[s("span",{style:{color:"#ABB2BF"}},"    bot "),s("span",{style:{color:"#56B6C2"}},"="),s("span",{style:{color:"#ABB2BF"}}," "),s("span",{style:{color:"#61AFEF"}},"get_bot"),s("span",{style:{color:"#ABB2BF"}},"()")]),l(`
`),s("span",{class:"line"},[s("span",{style:{color:"#ABB2BF"}},"    version "),s("span",{style:{color:"#56B6C2"}},"="),s("span",{style:{color:"#ABB2BF"}}," "),s("span",{style:{color:"#C678DD","font-style":"italic"}},"await"),s("span",{style:{color:"#ABB2BF"}}," bot."),s("span",{style:{color:"#61AFEF"}},"get_version"),s("span",{style:{color:"#ABB2BF"}},"()")]),l(`
`),s("span",{class:"line"}),l(`
`),s("span",{class:"line"})])])],-1);function R(S,U){const B=p("Badge"),c=p("Tabs");return y(),i("div",null,[F,d,s("h2",_,[C,l(" 获取最新事件列表"),a(B,{text:"标准",type:"success"})]),u,g,a(c,{id:"17",data:[{title:"请求参数"},{title:"响应数据"},{title:"请求示例"},{title:"响应示例"},{title:"在nb2使用"}]},{tab0:n(({title:o,value:e,isActive:t})=>[b]),tab1:n(({title:o,value:e,isActive:t})=>[h]),tab2:n(({title:o,value:e,isActive:t})=>[x]),tab3:n(({title:o,value:e,isActive:t})=>[v]),tab4:n(({title:o,value:e,isActive:t})=>[m]),_:1}),s("h2",E,[f,l(" 获取支持的动作列表"),a(B,{text:"标准",type:"success"})]),D,a(c,{id:"89",data:[{title:"请求参数"},{title:"响应数据"},{title:"请求示例"},{title:"响应示例"},{title:"在nb2使用"}]},{tab0:n(({title:o,value:e,isActive:t})=>[k]),tab1:n(({title:o,value:e,isActive:t})=>[w]),tab2:n(({title:o,value:e,isActive:t})=>[j]),tab3:n(({title:o,value:e,isActive:t})=>[O]),tab4:n(({title:o,value:e,isActive:t})=>[T]),_:1}),s("h2",q,[N,l(" 获取运行状态"),a(B,{text:"标准",type:"success"})]),V,a(c,{id:"116",data:[{title:"请求参数"},{title:"响应数据"},{title:"请求示例"},{title:"响应示例"},{title:"在nb2使用"}]},{tab0:n(({title:o,value:e,isActive:t})=>[W]),tab1:n(({title:o,value:e,isActive:t})=>[H,P,X]),tab2:n(({title:o,value:e,isActive:t})=>[Y]),tab3:n(({title:o,value:e,isActive:t})=>[Z]),tab4:n(({title:o,value:e,isActive:t})=>[$]),_:1}),s("h2",z,[G,l(" 获取版本信息"),a(B,{text:"标准",type:"success"})]),I,a(c,{id:"221",data:[{title:"请求参数"},{title:"响应数据"},{title:"请求示例"},{title:"响应示例"},{title:"在nb2使用"}]},{tab0:n(({title:o,value:e,isActive:t})=>[J]),tab1:n(({title:o,value:e,isActive:t})=>[K]),tab2:n(({title:o,value:e,isActive:t})=>[L]),tab3:n(({title:o,value:e,isActive:t})=>[M]),tab4:n(({title:o,value:e,isActive:t})=>[Q]),_:1})])}const ls=r(A,[["render",R],["__file","meta.html.vue"]]);export{ls as default};
