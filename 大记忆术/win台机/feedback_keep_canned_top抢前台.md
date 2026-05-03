---
name: keep_canned_top.sh 守护脚本会误抢用户切的前台窗口
description: neo 04-30 实证 keep_canned_top.sh 在发文期会把用户切到的 Terminal/其他窗口立刻弹回罐头;neo2/air 没装也不抢,可能本就非必要
type: feedback
originSessionId: 231b8291-86e8-48aa-b91b-26f7b22ff45c
---
`/tmp/keep_canned_top.sh`(v1101.3 hotfix#2)在某些机器上**会误抢用户主动切的前台窗口** — 用户切 Terminal 后 1 秒内被弹回创作罐头,严重影响多任务。

**Why:** 2026-04-30 11:00 缺哥反馈 neo 发文期"无法切其他窗口,总弹回罐头",neo2/air 同期不抢。实证差异:
- neo 上跑 2 份 keep_canned_top.sh 守护(PID 2824 + 77543,可能两次部署叠加)
- neo2 / mini / air 没跑这个守护(neo2 在跑发文也不抢 = 守护非必要)

脚本写得是 `pgrep gtg_batch|gtg_timer + frontmost=Finder` 双条件才 activate,理论不该误抢。但实测在 cliclick / 罐头窗口切换瞬间 frontmost 短暂变 Finder,守护命中 → activate 罐头 → 用户的 Terminal frontmost 被打掉。0.5s 轮询 + 2 份并发让窗口期极短。

**How to apply:**
1. 用户报"无法切窗口"时,先 ssh 该机 `ps aux | grep keep_canned_top.sh | grep -v grep`,有就 `pkill -f keep_canned_top.sh`,验证现象消失。
2. 部署这个守护前先想清楚:目前 neo2 / air 没装也不抢前台,**可能这个守护本就非必要**;若要装,需先加白名单(Terminal/iTerm/VSCode 等 frontmost 时不动 + 防抖 N 次 Finder 才 activate),避免短瞬切窗误抢。
3. 如果 mac 端 Finder 兜底问题再次出现,再考虑装(memory hotfix#2 当时是为 air 的"罐头被推到桌面后台"加的)。
4. 部署多次时务必 `pkill` 老进程再启,不要叠加。

---

## v2 白名单版(2026-05-03 落地全 4 Mac)

**触发:** 2026-05-03 NEO 9h19m 文章定时全失败(199 次「文档导入弹窗未出现」),根因罐头窗口偶发被推到后台/失焦,cliclick 物理点击落到别的窗口;缺哥手动激活罐头后立刻恢复 → 反复发生。同期 AIR/NEO2/MINI 已装 v1 守护(无白名单)反向问题:缺哥要切 Finder/VS Code 看文件就被弹回。

**v2 修法:** 守护脚本加白名单 + 防抖。脚本路径:`~/keep_canned_top_v2.sh`,日志 `~/keep_canned_top.log`。

**白名单(缺哥拍):**
- VS Code(`Code`/`Cursor`)
- 微信(`WeChat`)
- 访达(`Finder`)— **首要,缺哥要看文件**
- Tailscale
- Shadowrocket
- Terminal / iTerm2(查 log 用)
- 罐头自身(`创作罐头`,已 frontmost 不需再 activate)

**核心逻辑:**
- 1s 轮询 `osascript "tell System Events to get name of first process whose frontmost is true"`
- frontmost 不在白名单 → 计数 +1;连续 3 次(防抖)→ activate 罐头
- frontmost 在白名单 → 计数清零,不抢
- 仅 `pgrep -f gtg_batch|gtg_timer` 命中(发文期)才生效,不发文不抢

**部署铁律:**
- 部署前必 `pkill -f keep_canned_top` 杀旧版,**严禁 v1/v2 叠加**(04-30 NEO 跑过 2 份导致防抖失效)
- 用 nohup 后台跑,无 tty 也能存活
- 5 机统一(NEO 首装,AIR/NEO2/MINI 替换 v1)

**调白名单时机:** 缺哥说"被抢"=漏 app,加进 WHITELIST;缺哥说"罐头跑飞"=守护没救回来,降 DEBOUNCE 或缩 SLEEP。
