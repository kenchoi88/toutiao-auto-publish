---
name: feedback-collect-accounts-b
description: "台机 collect_accounts B 方案 — 主循环 same_count 容错 + 兜底循环, 稳定换速度 (15s → 40-60s 但保证全收)"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 6590fd21-264a-4cca-9599-9b4151b2ee6a
---

台机 (微头条 / 文章自动 / 文章定时辅助) collect_accounts 用 **B 方案**:

```python
# 主循环: same_count 容错避免 loading 中误判到底
same_count = 0
for _ in range(1000):
    扫 + 累加
    滚 200px
    time.sleep(0.5)              # 0.3 → 0.5 多等 lazy render
    if before == after:
        same_count += 1
        if same_count >= 4:      # 连续 4 次不动才认定到底
            break
    else:
        same_count = 0

# 兜底循环: 滚到底 + 等 2s + 扫, 直到连续 3 次没新增 (最多 20 轮)
no_new_count = 0
bottom_round = 0
while no_new_count < 3 and bottom_round < 20:
    bottom_round += 1
    强制滚到底
    time.sleep(2.0)              # 给 lazy render 充分时间
    扫
    if 新增 > 0:
        no_new_count = 0
        log(f"兜底第 {bottom_round} 轮: 补收 {added} 个 (累计 N)")
    else:
        no_new_count += 1
```

**Why:**
2026-05-16 18:53 台机文章定时启动, collect 出 240 个账号, 实际罐头侧栏 304 个, 漏 64 个。

根因:
- V1102.8 win 简化的 `if before_top == after_top: break` 没 loading 容错
- 罐头侧栏虚拟滚动 lazy render 中, scrollTop 暂时不变 → 误判到底 → 提前 break
- 原兜底「滚到底再扫一次」只补 20 个, 远不够 304 场景

缺哥手动滚到底再启动 → collect 出 304 ✓ — 证明 DOM 实际有 304, 是 collect 提前结束。

**台机比 mac 账号多** (mac 120-122 / 台机 304), 需要更稳的兜底。

**How to apply:**
- 台机三件 collect_accounts 函数体 (微头条 + 文章自动 + 文章定时辅助 gtg_batch) 用 B 方案
- mac 三件保留 V1102.7 mac 原版的 has_scrolled + same_count >= 6 (实测 120-122 都 OK, 不强加 B 方案)
- 代价:collect 时间从 ~15s 变 **~40-60s**, 缺哥拍「慢就慢」(2026-05-16)
- 不要为图快回退到 `if before == after: break` 单条件 — 会再次漏账号
- 微调参数 (sleep 0.5/2.0 + same_count 4 + no_new_count 3) 是稳定档, 改快任一参数都可能漏

**实证 (V1103 落地后)**:
- 台机文章定时 18:56 启动: collect 出 **304 个账号** ✓
- 早窗 304 + 中窗 304 + 晚窗 304 = 共 912 任务 ✓
- 余 0 篇 (912 素材 / 304 全员 = quota=3 整除)

**关联:**
- V1103 版本说明: `自动发布/自动发布V1103/V1103版本说明.txt` 第三节 collect_accounts B 方案
- 故障说明 5/16 故障 9
- WIN/MAC 不可跨推: [[feedback_WIN_MAC不可跨推]]
- 罐头爆款下载也用 collect (但是另一个 selector): [[reference_罐头爆款下载流程]]
