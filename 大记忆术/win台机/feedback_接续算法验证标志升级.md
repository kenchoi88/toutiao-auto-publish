---
name: feedback
description: "V1102.6 接续算法 5 天伪生效暴露 — 验证标志必须 log YY ≡ 首篇 publish ZZ 双锁, 不能只看 log"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 6590fd21-264a-4cca-9599-9b4151b2ee6a
---

接续算法 (V1102.6 移出 if _wl_q 块) 真生效的验证标志:

**log 「中断处自动接续:从下一位 YY 起跑」 + 首篇 publish ZZ 实际账号名 == YY**

只看 log 不算通过 — log 写得对不等于实际行为对。

**Why:**
V1102.6 (2026-05-10) 实证标志只看 log 出 `[v1102.6] 中断处自动接续:从下一位 YY 起跑` 就算通过, 左右 + 缺哥 5/10 都被这个标志骗了。实际 `_is_eligible` 里 `name not in sent_accounts_set` 检查会让接续点账号 (本轮已发部分) 被跳过, 真正首篇 publish 是顺位下一个 0 篇账号 ZZ ≠ YY。这个伪生效跑了 5 天 (5/10-5/16) 没暴露, 因为实证场景接续点账号本轮恰好没发过, 跳过逻辑不触发。

5/16 mini 14:43 socket 异常崩 + 缺哥重启暴露:接续点账号本轮已发 2 篇 → 在 sent_accounts_set → _is_eligible 跳过 → 首篇 publish ≠ YY。

**How to apply:**
- 审接续算法相关任何 patch 必看 2 个 log 行:
  1. `中断处自动接续:从下一位 YY 起跑` (算法层输出)
  2. `[剩余 N 篇] [大1/小M/A] ZZ -> ...docx` (实际首篇 publish)
- 必须 YY ≡ ZZ 才算真接续, 缺一不可
- 即使 YY ≡ ZZ 也要看「接续点账号本轮已发部分篇数」边界场景 (本轮已发 0 / 1 / 2 / 已满 quota 都要覆盖)
- 验证用 `until + tail -50 log + grep "接续 + 首篇" 双锁` 自动判定

**关联:**
- V1103 版本说明: `自动发布/自动发布V1103/V1103版本说明.txt` 第一节改动 1
- 故障说明: `自动发布/故障说明/故障说明_2026-05-16.txt` 故障 1
- 旧记忆 V1102.6 完整 (neo2 左右): `大记忆术/neo2/project_V1102_6完整_5_10.md`
- 跨件适用: 微头条 / 文章自动 / 文章定时 三件接续算法都按此标志验
