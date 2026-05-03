---
name: v1101.3 已推 mini/air/neo2,新会话别再重复 push
description: v1101.3 三大件 patch 在 2026-04-29 21:37 已落地 mini/air/neo2,顶部注释可能没换("[v1101] 大统一基线"是误导),实机 .bak_pre_v1101.3_20260429_* 是落地证据
type: feedback
originSessionId: 231b8291-86e8-48aa-b91b-26f7b22ff45c
---
v1101.3 三大件 hotfix 在 **2026-04-29 21:37 已推完** mini / air / neo2(neo 当时 offline 待补),备份在各机 `~/Desktop/{微头条/文章/文章定时}自动发布/<py>.bak_pre_v1101.3_20260429_*`。

**Why:** 2026-04-30 早晨,我在新会话里看 mini 上 gtg_batch.py 顶部注释还是 `[v1101] 大统一基线 — Step 3 6s 删 + ProseMirror...`,误判 mini 没升 v1101.3。从 neo2 拉一份覆盖 mini 三件,把 mini 自家 v1101.3 patch(微头条/文章 md5 与 neo2 不同)替换成 neo2 版,污染本机微调。缺哥大怒,要求回滚 + 写 memory 防再犯。

**How to apply:** 跨会话遇到"该机版本是否最新"问题:
1. **先 ssh 列 .bak**:`ls ~/Desktop/*/gtg_*.py.bak_pre_v1101.X_*` —— 04-29 21:37 时间戳的 .bak 在 = 当时确实推过。
2. **再 grep patch 标记**(不光看顶部注释):`grep -cE "v1101\.3|cb 真坐标|首发复选框|硬保护|校准失败" file.py` —— >0 = patch 已落,顶部注释可能滞后。
3. **md5 对比再决策**:同一 patch 不同分支(mini 自 patch / 从 neo2 拉)会出现 md5 不同但语义等价 —— 不要贸然覆盖,先 diff。
4. 看到 neo offline 这种待补项,留着等它上电再补,别擅自跨机拉同步覆盖。
