import{_ as i,W as y,X as d,Y as s,Z as e,$ as a,a0 as l,a1 as _,D as c}from"./framework-a17ef302.js";const A={},F=s("h1",{id:"消息动作",tabindex:"-1"},[s("a",{class:"header-anchor",href:"#消息动作","aria-hidden":"true"},"#"),e(" 消息动作")],-1),g={id:"发送消息",tabindex:"-1"},u=s("a",{class:"header-anchor",href:"#发送消息","aria-hidden":"true"},"#",-1),h=_('<p>action: <code>send_message</code></p><div class="hint-container warning"><p class="hint-container-title">Wechat</p><p>由于 wechat 的特性，该接口有以下限制:</p><ul><li><code>message_type</code> 只能为 <code>private</code> 或 <code>group</code></li><li><code>message</code> 中的每个消息段都将作为一条消息发送出去(除了<code>mention</code>)</li><li><code>mention</code> 和 <code>mention_all</code> 只支持群聊</li></ul></div>',2),C=s("thead",null,[s("tr",null,[s("th",{style:{"text-align":"center"}},"字段名"),s("th",{style:{"text-align":"center"}},"数据类型"),s("th",{style:{"text-align":"center"}},"说明")])],-1),m=s("tr",null,[s("td",{style:{"text-align":"center"}},[s("code",null,"message_type")]),s("td",{style:{"text-align":"center"}},"string"),s("td",{style:{"text-align":"center"}},[e("消息类型，"),s("code",null,"private"),e(" 或 "),s("code",null,"group")])],-1),x=s("tr",null,[s("td",{style:{"text-align":"center"}},[s("code",null,"user_id")]),s("td",{style:{"text-align":"center"}},"string"),s("td",{style:{"text-align":"center"}},[e("用户 ID，当 "),s("code",null,"detail_type"),e(" 为 "),s("code",null,"private"),e(" 时必须传入")])],-1),b=s("tr",null,[s("td",{style:{"text-align":"center"}},[s("code",null,"group_id")]),s("td",{style:{"text-align":"center"}},"string"),s("td",{style:{"text-align":"center"}},[e("群 ID，当 "),s("code",null,"detail_type"),e(" 为 "),s("code",null,"group"),e(" 时必须传入")])],-1),f=s("td",{style:{"text-align":"center"}},[s("code",null,"message")],-1),v=s("td",{style:{"text-align":"center"}},"message",-1),E={style:{"text-align":"center"}},D=s("p",null,[e("在 "),s("code",null,"Onebot12"),e(" 标准中，原则上应该返回一个 "),s("code",null,"message_id"),e("，但是由于hook的限制，目前只能返回一个 "),s("code",null,"bool"),e("，用来判断消息是否发送成功。")],-1),k=s("div",{class:"language-json","data-ext":"json"},[s("pre",{class:"shiki one-dark-pro",style:{"background-color":"#282c34"},tabindex:"0"},[s("code",null,[s("span",{class:"line"},[s("span",{style:{color:"#ABB2BF"}},"{")]),e(`
`),s("span",{class:"line"},[s("span",{style:{color:"#ABB2BF"}},"    "),s("span",{style:{color:"#E06C75"}},'"action"'),s("span",{style:{color:"#ABB2BF"}},": "),s("span",{style:{color:"#98C379"}},'"send_message"'),s("span",{style:{color:"#ABB2BF"}},",")]),e(`
`),s("span",{class:"line"},[s("span",{style:{color:"#ABB2BF"}},"    "),s("span",{style:{color:"#E06C75"}},'"params"'),s("span",{style:{color:"#ABB2BF"}},": {")]),e(`
`),s("span",{class:"line"},[s("span",{style:{color:"#ABB2BF"}},"        "),s("span",{style:{color:"#E06C75"}},'"detail_type"'),s("span",{style:{color:"#ABB2BF"}},": "),s("span",{style:{color:"#98C379"}},'"group"'),s("span",{style:{color:"#ABB2BF"}},",")]),e(`
`),s("span",{class:"line"},[s("span",{style:{color:"#ABB2BF"}},"        "),s("span",{style:{color:"#E06C75"}},'"group_id"'),s("span",{style:{color:"#ABB2BF"}},": "),s("span",{style:{color:"#98C379"}},'"12467"'),s("span",{style:{color:"#ABB2BF"}},",")]),e(`
`),s("span",{class:"line"},[s("span",{style:{color:"#ABB2BF"}},"        "),s("span",{style:{color:"#E06C75"}},'"message"'),s("span",{style:{color:"#ABB2BF"}},": [")]),e(`
`),s("span",{class:"line"},[s("span",{style:{color:"#ABB2BF"}},"            {")]),e(`
`),s("span",{class:"line"},[s("span",{style:{color:"#ABB2BF"}},"                "),s("span",{style:{color:"#E06C75"}},'"type"'),s("span",{style:{color:"#ABB2BF"}},": "),s("span",{style:{color:"#98C379"}},'"text"'),s("span",{style:{color:"#ABB2BF"}},",")]),e(`
`),s("span",{class:"line"},[s("span",{style:{color:"#ABB2BF"}},"                "),s("span",{style:{color:"#E06C75"}},'"data"'),s("span",{style:{color:"#ABB2BF"}},": {")]),e(`
`),s("span",{class:"line"},[s("span",{style:{color:"#ABB2BF"}},"                    "),s("span",{style:{color:"#E06C75"}},'"text"'),s("span",{style:{color:"#ABB2BF"}},": "),s("span",{style:{color:"#98C379"}},'"我是文字巴拉巴拉巴拉"')]),e(`
`),s("span",{class:"line"},[s("span",{style:{color:"#ABB2BF"}},"                }")]),e(`
`),s("span",{class:"line"},[s("span",{style:{color:"#ABB2BF"}},"            }")]),e(`
`),s("span",{class:"line"},[s("span",{style:{color:"#ABB2BF"}},"        ]")]),e(`
`),s("span",{class:"line"},[s("span",{style:{color:"#ABB2BF"}},"    }")]),e(`
`),s("span",{class:"line"},[s("span",{style:{color:"#ABB2BF"}},"}")]),e(`
`),s("span",{class:"line"})])])],-1),j=s("div",{class:"language-json","data-ext":"json"},[s("pre",{class:"shiki one-dark-pro",style:{"background-color":"#282c34"},tabindex:"0"},[s("code",null,[s("span",{class:"line"},[s("span",{style:{color:"#ABB2BF"}},"{")]),e(`
`),s("span",{class:"line"},[s("span",{style:{color:"#ABB2BF"}},"    "),s("span",{style:{color:"#E06C75"}},'"status"'),s("span",{style:{color:"#ABB2BF"}},": "),s("span",{style:{color:"#98C379"}},'"ok"'),s("span",{style:{color:"#ABB2BF"}},",")]),e(`
`),s("span",{class:"line"},[s("span",{style:{color:"#ABB2BF"}},"    "),s("span",{style:{color:"#E06C75"}},'"retcode"'),s("span",{style:{color:"#ABB2BF"}},": "),s("span",{style:{color:"#D19A66"}},"0"),s("span",{style:{color:"#ABB2BF"}},",")]),e(`
`),s("span",{class:"line"},[s("span",{style:{color:"#ABB2BF"}},"    "),s("span",{style:{color:"#E06C75"}},'"data"'),s("span",{style:{color:"#ABB2BF"}},": "),s("span",{style:{color:"#D19A66"}},"true"),s("span",{style:{color:"#ABB2BF"}},",")]),e(`
`),s("span",{class:"line"},[s("span",{style:{color:"#ABB2BF"}},"    "),s("span",{style:{color:"#E06C75"}},'"message"'),s("span",{style:{color:"#ABB2BF"}},": "),s("span",{style:{color:"#98C379"}},'""')]),e(`
`),s("span",{class:"line"},[s("span",{style:{color:"#ABB2BF"}},"}")]),e(`
`),s("span",{class:"line"})])])],-1),w=s("div",{class:"language-python","data-ext":"py"},[s("pre",{class:"shiki one-dark-pro",style:{"background-color":"#282c34"},tabindex:"0"},[s("code",null,[s("span",{class:"line"},[s("span",{style:{color:"#C678DD","font-style":"italic"}},"from"),s("span",{style:{color:"#ABB2BF"}}," nonebot.adapters.onebot.v12 "),s("span",{style:{color:"#C678DD","font-style":"italic"}},"import"),s("span",{style:{color:"#ABB2BF"}}," Bot, MessageSegment")]),e(`
`),s("span",{class:"line"},[s("span",{style:{color:"#C678DD","font-style":"italic"}},"from"),s("span",{style:{color:"#ABB2BF"}}," nonebot "),s("span",{style:{color:"#C678DD","font-style":"italic"}},"import"),s("span",{style:{color:"#ABB2BF"}}," get_bot")]),e(`
`),s("span",{class:"line"}),e(`
`),s("span",{class:"line"},[s("span",{style:{color:"#C678DD"}},"async"),s("span",{style:{color:"#ABB2BF"}}," "),s("span",{style:{color:"#C678DD"}},"def"),s("span",{style:{color:"#ABB2BF"}}," "),s("span",{style:{color:"#61AFEF"}},"test"),s("span",{style:{color:"#ABB2BF"}},"():")]),e(`
`),s("span",{class:"line"},[s("span",{style:{color:"#ABB2BF"}},"    bot "),s("span",{style:{color:"#56B6C2"}},"="),s("span",{style:{color:"#ABB2BF"}}," "),s("span",{style:{color:"#61AFEF"}},"get_bot"),s("span",{style:{color:"#ABB2BF"}},"()")]),e(`
`),s("span",{class:"line"},[s("span",{style:{color:"#ABB2BF"}},"    message "),s("span",{style:{color:"#56B6C2"}},"="),s("span",{style:{color:"#ABB2BF"}}," MessageSegment."),s("span",{style:{color:"#61AFEF"}},"text"),s("span",{style:{color:"#ABB2BF"}},"("),s("span",{style:{color:"#98C379"}},'"我是文字巴拉巴拉巴拉"'),s("span",{style:{color:"#ABB2BF"}},") "),s("span",{style:{color:"#56B6C2"}},"+")]),e(`
`),s("span",{class:"line"},[s("span",{style:{color:"#ABB2BF"}},"              MessageSegment."),s("span",{style:{color:"#61AFEF"}},"image"),s("span",{style:{color:"#ABB2BF"}},"("),s("span",{style:{color:"#E06C75","font-style":"italic"}},"file_id"),s("span",{style:{color:"#56B6C2"}},"="),s("span",{style:{color:"#98C379"}},'"asd-asd-asd-ads"'),s("span",{style:{color:"#ABB2BF"}},")")]),e(`
`),s("span",{class:"line"},[s("span",{style:{color:"#ABB2BF"}},"    "),s("span",{style:{color:"#C678DD","font-style":"italic"}},"await"),s("span",{style:{color:"#ABB2BF"}}," bot."),s("span",{style:{color:"#61AFEF"}},"send_message"),s("span",{style:{color:"#ABB2BF"}},"("),s("span",{style:{color:"#E06C75","font-style":"italic"}},"detail_type"),s("span",{style:{color:"#56B6C2"}},"="),s("span",{style:{color:"#98C379"}},'"group"'),s("span",{style:{color:"#ABB2BF"}},","),s("span",{style:{color:"#E06C75","font-style":"italic"}},"group_id"),s("span",{style:{color:"#56B6C2"}},"="),s("span",{style:{color:"#98C379"}},'"12467"'),s("span",{style:{color:"#ABB2BF"}},","),s("span",{style:{color:"#E06C75","font-style":"italic"}},"message"),s("span",{style:{color:"#56B6C2"}},"="),s("span",{style:{color:"#ABB2BF"}},"message)")]),e(`
`),s("span",{class:"line"}),e(`
`),s("span",{class:"line"})])])],-1),N={id:"撤回消息",tabindex:"-1"},S=s("a",{class:"header-anchor",href:"#撤回消息","aria-hidden":"true"},"#",-1),V=s("p",null,[e("action: "),s("code",null,"delete_message")],-1),M=s("div",{class:"hint-container danger"},[s("p",{class:"hint-container-title"},"Wechat"),s("p",null,"未实现该动作。")],-1);function T(W,I){const r=c("Badge"),B=c("RouterLink"),p=c("Tabs");return y(),d("div",null,[F,s("h2",g,[u,e(" 发送消息"),a(r,{text:"标准",type:"success"})]),h,a(p,{id:"31",data:[{title:"请求参数"},{title:"响应数据"},{title:"请求示例"},{title:"响应示例"},{title:"在nb2使用"}]},{tab0:l(({title:t,value:o,isActive:n})=>[s("table",null,[C,s("tbody",null,[m,x,b,s("tr",null,[f,v,s("td",E,[e("消息内容，为消息段列表，详见 "),a(B,{to:"/message/"},{default:l(()=>[e("消息段")]),_:1})])])])])]),tab1:l(({title:t,value:o,isActive:n})=>[D]),tab2:l(({title:t,value:o,isActive:n})=>[k]),tab3:l(({title:t,value:o,isActive:n})=>[j]),tab4:l(({title:t,value:o,isActive:n})=>[w]),_:1}),s("h2",N,[S,e(" 撤回消息"),a(r,{text:"标准",type:"success"})]),V,M])}const R=i(A,[["render",T],["__file","message.html.vue"]]);export{R as default};
