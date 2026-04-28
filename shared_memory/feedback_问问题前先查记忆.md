---
name: 问缺哥 / 让缺哥做事 之前,先读记忆 + 仓库
description: 反射动作 — 提问、回"不知道"、让缺哥手动跑命令、想 brute force 之前,先 grep memory + 看仓库 shared_memory/版本说明/故障日志
type: feedback
originSessionId: f99b6b5b-4ea0-48d9-baf7-b1b507d56ce3
---

**规则:** 每次准备问缺哥问题、或回答"不知道 / 不清楚 / 还没确认"、**或让缺哥手动做事(跑命令、点链接、登录某个东西、改配置)之前**,必须先查两处:

1. **本机记忆** — `~/.claude/projects/.../memory/` 全部 .md(grep 关键词)
2. **仓库** — `shared_memory/*.md`(跨机共享)+ `自动发布/版本说明.txt`(版本约定)+ `自动发布/故障日志.txt`(跨机 bug 跟踪)

记忆 / 仓库里有就直接用,没有再问。

**Why:**
- 2026-04-27 给 neo / neo2 装 Tailscale 时:SSH 用户名规律早记 memory,我没查就 brute force 7 个候选;5 台机统一密码也记了,还反复问缺哥重发。
- 2026-04-28 晚:缺哥让我自查 mini v1101.1,我先入为主以为有"假目录"问题,折腾 patch dry-run / EOL 转换 — 其实仓库 `shared_memory/project_v1101_spec.md` + `自动发布/版本说明.txt` 已经把 v1101 / v1101.1 关系讲清楚,我看完就该懂"v1101 是基线 + v1101.1 是熔断重构 6 条增量",根本不用走 diff/patch 弯路。
- 让缺哥点 ts-ssh 网页认证 / 重启 SR / 改 firewall 这种"让缺哥做事"的请求,80% 在记忆/仓库已有更聪明的替代路径或已被定调"暂搁",发出去就是浪费缺哥时间 + 挨骂。

**How to apply:**
- 想问 SSH 用户名 / 密码 / IP / 端口 / 账号 前 → 先 grep memory + reference_*
- 想说"待确认 / 你告诉我"之前 → 先 grep memory + 仓库 shared_memory + 版本说明.txt + 故障日志.txt
- 想 brute force 试错之前 → 有规律先套规律
- **想让缺哥手动跑命令 / 点链接 / 改配置之前** → 先查记忆 + 仓库,看是否已有定调("等左右上线再说"、"明天再搞"),或已有更聪明的替代;**别让缺哥反复点同一个 ts-ssh 认证 URL / 反复确认同件事**
- 已知会随时间过期的(项目状态、IP 表、版本进度)— 用之前快速验证,但**默认是已记**,不是"重新问一遍"
- memory / 仓库找不到才问,问完立刻把答案补进 memory(下次别再问)
