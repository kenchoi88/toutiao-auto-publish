---
name: 跨机连通+SSH 真通的最新基线(2026-04-28 21:51 实测 5 机全开)
description: 测连通报"通"就够;缺哥让查具体内容必须实地 SSH 进去验,commit/session log 是间接证据会臆想翻车;ts-ssh 拦先等再试别马上劝退
type: feedback
originSessionId: cb9a7602-be16-4ed3-a1d1-8c5296bb337e
---

## 现在的事实(2026-04-28 21:51 真测,记进脑子)

**5 机 SSH 真握手 + 执行命令全通**(从 Win 台机出方向):

| 机 | 代号 | SSH 命令 | hostname | 用户 |
|---|---|---|---|---|
| ken-choi(本机) | 绣虎 | — | — | kench |
| air | 阿良 | `ssh kenair@100.67.252.1` | KendeMacBook-Air.local | kenair |
| neo | 小齐+小师弟 | `ssh kenchoios@100.68.57.96` | kenchoiosdeMacBook.local | kenchoios |
| mini | 东山 | `ssh kenchoimini@100.70.22.7` | KenChoideMac-mini.local | kenchoimini |
| neo2 | 左右 | `ssh kenchoineo2@100.96.153.17` | KenChoineo2deMacBook.local | kenchoineo2 |

⚠️ **air = `kenair`**(不是 kenchoiair),**neo = `kenchoios`**(不是 kenchoineo)— 两个例外详见 `reference_SSH用户名规律.md`,别再 brute force。

## 报告规则

- 缺哥说"测各机器通不通" → ICMP + TCP/22,5 台报"通"完事,不要列谁 ICMP 不回当故障(TCP 通即可用,业务全走 TCP)
- 缺哥说"确认 X 件 v1101.1 落实" / "查 mac 三大件" → **必须实地 SSH 进去 grep**;commit message 自述 / session log 反向 scp 痕迹都是间接证据,**会臆想翻车**(2026-04-28 晚翻过两次车)
- 报告时不要把"ICMP 不通 / 某机 ts-ssh 拦"挂在开头当包袱;通就是通

## ts-ssh 网页认证 ≠ hard-stop

- 2026-04-28 晚上一段时间 air/mini/neo2 都拦"Tailscale SSH requires an additional check",我以为彻底 hard-stop,劝退缺哥"等对端 Claude"。错。
- 实际:缺哥任何 admin console 操作 / 浏览器同账号登录任一处都会刷新整个 tailnet 的 SSH 身份,所有 ts-ssh tagged mac **同时解锁**。一次操作 = 全员开。
- **看到 ts-ssh 拦先等一会重试**(缺哥可能正在 admin / 浏览器操作),别一拦就劝退。隔几分钟再试一次。
- 例外只在两种情况:① 反复重试连续拦 30 分钟以上 ② 对端 wrapper 之外另有问题(网络断/sshd 死) — 此时再回报"对端拦"

## Why 这条记忆存在

2026-04-28 翻车记录:
- 自查 v1101.1 假目录:仓库代码 grep "v1101.1" = 0 处就臆想"假货",其实仓库已合 v1101 P3/P5/P6/P7 真版,只是 v1101.1 增量(熔断重构 6 条)还没合。看一眼 `版本说明.txt`(仓库根)就懂,我没看就编叙事
- 自查 mini 三大件:不实地 SSH 凭间接证据反复说"mac 全是新版本",最后 SSH 进去发现 mini 微头条桌面停在 v1101 没合 v1101.1 增量
- 都源于"不进对端 grep / 信任工作流"的过度自信。**纠偏:缺哥让查就实地查,实地证据 > 任何间接推断**
