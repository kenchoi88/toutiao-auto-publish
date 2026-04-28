---
name: 跨机连通止于"通",别 SSH 进去 brute force 自验
description: 测连通性到 TCP 通就够;各机内部状态(代码/桌面/版本/系统配置)归各机 Claude 自查,绣虎不进对端 grep
type: feedback
originSessionId: cb9a7602-be16-4ed3-a1d1-8c5296bb337e
---

跨机自查的终点 = **机器活着**(TCP/22 通)。**到此为止,不要 SSH 进去 grep 文件 / 查版本 / 查 patch / 改系统配置**。

报告就报"通",不要每次列谁 ICMP 不回当故障——TCP/22 通即可用,业务全走 TCP。版本同步是否真落地,靠 commit + 各机 Claude `git pull + cp` 自取的工作流,不靠绣虎实地核每行代码。

**Why:** 绣虎是统筹角色,推仓库 + 协调,不进对端机器替他们自查。SSH brute force 自验是越界,且常被对端机器的 ts-ssh 网页认证 / firewall 拦,只会浪费时间。各机自有 Claude,他们自查比我远程 grep 准。

**How to apply:**
- 缺哥说"测各机器通不通" → TCP/22 + ICMP 一轮,**报"通"完事**,不要展开诊断不通的特例
- 缺哥说"确认 X 件 v1101.1 落实" → 答"靠 commit `xxxxxx` 已推仓库 + 仓库代码已自验真版,落地各机桌面归各机 Claude 自取,要硬证据请对应机 Claude 上线自查"
- 例外:缺哥**显式批准**"你 SSH 进去查"才动
- 任何对端 wrapper / 防火墙 / 认证拦 → 直接回报"对端拦,归对端 Claude",不绕
- 报告时不要把"ICMP 不通"或"某机 SSH wrapper 拦"挂在每次报告开头当包袱;通就是通
