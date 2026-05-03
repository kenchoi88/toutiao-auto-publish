---
name: 靠证据查问题，不要瞎想
description: 排查时用实际状态（env/注册表/配置文件/命令输出）说话，不要脑补历史或推测别人做了什么
type: feedback
originSessionId: bf890c87-5454-4ee3-ba3f-781f6d8dff55
---
排查问题一律**拿实际证据定病因**，不要拿「可能阿良做了 X」「可能是 IPv6 导致」这类空想下结论。

**Why:** 本次事故早期我把「阿良昨晚关 IPv6」脑补成「为了修视频」，还基于错误因果链给出建议，被崔巉当场驳回（"历史是不对的"）。真正病因最后靠一条 `Get-ChildItem Env:` 命令锁定 —— 是持久化的 `HTTPS_PROXY` 环境变量，跟 IPv6 一毛钱关系没有。时间全花在脑补和复述上。

**How to apply:**
- 先查实际状态：`Get-ChildItem Env:`、`Get-ItemProperty HKCU:\...InternetSettings`、`Get-NetAdapterBinding`、读配置文件、看进程列表/监听端口。
- 证据足够前不下结论、不推荐方案。
- 讲历史只说用户直接讲过的事实；不要基于历史"推理"因果链并当事实用。
- 用户说「历史是不对的」「你弄错了」—— 立刻停止推测，让用户给事实，而不是继续猜。
- 推荐方案必须映射到具体证据（"因为 User 级环境变量 HTTPS_PROXY 存在，所以..."），不能是"可能是代理残留"这种虚词。
