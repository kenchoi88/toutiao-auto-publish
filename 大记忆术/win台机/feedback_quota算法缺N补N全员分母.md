---
name: feedback-quota-n-n
description: "V1103 quota 算法统一 — (素材+已发)//全员账号 整除, 余数留素材池, 无 cap, sub_rounds 动态对齐"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 6590fd21-264a-4cca-9599-9b4151b2ee6a
---

quota 算法**死规则**(V1103 5/16 缺哥拍, 全 5 机三件统一):

```python
_full_accounts_count = len(accounts)       # EXCLUDE_ACCOUNTS 过滤后保留全员数
# ... 白名单优先排序 (但不剔除) ...
_quota_per = max(1, (len(docs) + sent_total) // _full_accounts_count)
_quota_余 = (len(docs) + sent_total) % _full_accounts_count
quota_map = {a: _quota_per for a in accounts}
# sub_rounds 动态对齐
sub_rounds=_quota_per     # 或 sub_rounds=quota_total (文章定时 Stage 2)
```

**Why:**
缺哥拍核心需求 (5/16 多次确认):
- **总篇数 ÷ 总账号 = 每号 quota, 余数留素材池** ("除得尽就发, 除不尽留着")
- 总账号 = **全员** (collect 出 + EXCLUDE 过滤后), **不是白名单过滤后**
- 总篇数 = **素材池剩余 + 已发累计** (中断恢复时跟初次启动算式一致)
- **无 cap** — 历史 cap 5 / cap 3 是臆造的「平台硬上限」(V1102.2 line 211 注释), 平台实际无此限

例:
- 1000 素材 / 120 全员 → quota=8, 余 40 篇留素材池 (下次启动自然接续)
- 960 素材 / 120 全员 → quota=8, 余 0 篇 (刚好满)
- 912 素材 / 304 全员 → quota=3, 余 0 篇 (文章定时 3 时段恰好满)

老版踩过的坑 (V1103 之前):
1. **cap 5 / cap 3**: 缺哥要 10 篇/号被 cap 5 卡死 → 5/11 阿良改 5→10 / 5/15 缺哥拍取消 cap
2. **分母用 len(accounts)** (白名单过滤后) 而非全员 → 算出 quota 比应得小 1 → 漏 120 篇/天
3. **sub_rounds 写死** 跟 quota 不一致 → quota=8 但 sub_rounds=5 → 每号只发 5 篇 漏 3
4. **白名单剔除非白名单** → 不在白名单的账号不发 → catchup 写白名单基于 quota=5 剔除已满账号, 新 quota=8 后剔除的账号还能发 3 篇但被丢
5. **白名单 B 列 quota** (catchup 写「漏数」) 跟 main `acc_count<quota_map` 检查维度对冲 → 接续点已发账号立刻被跳

**How to apply:**
- 改任何 quota 相关代码前先核对此 5 项规则
- 白名单只**优先排序不剔除** (catchup 写白名单是「这些号优先, 其他号也发」), 不在白名单的账号追加 accounts 末尾
- 白名单 B 列 quota 忽略 (用户不手填 B 列, 写啥都没意义)
- 文章定时 timer 排程「物理 3 时段」 (早/中/晚) 是天然 cap 3, 但算法层 quota_total **不 cap** (取消 min(3, ...)), 让 Stage 2 死磕能补到 quota 满

**特殊件 — 文章定时**:
- Stage 1 _expand_tasks 物理 3 窗口 (早 q≥1 + 中 q≥2 + 晚 q≥3) — 不动
- Stage 2 死磕 sub_rounds=quota_total 动态 — V1103 新加 (mac 2849 行版有 Stage 2, 台机 600 行简化版无)
- mac 文章定时 quota=8 时: Stage 1 排 3 篇/号 + Stage 2 死磕补 5 篇/号 = 满 quota
- 台机简化版 无 Stage 2 → 每号实发 ≤ 3 篇 (Stage 1 物理上限), 剩余素材自然留素材池

**关联:**
- V1103 版本说明: `自动发布/自动发布V1103/V1103版本说明.txt` 第一节改动 2 + 3 + 4
- 故障说明 5/16 故障 3-6
- 旧版 cap 5/3 历史: [[project_发文上限与补漏规则]] (内容已被 V1103 覆盖, 旧值过时)
- 接续算法验证: [[feedback_接续算法验证标志升级]]
