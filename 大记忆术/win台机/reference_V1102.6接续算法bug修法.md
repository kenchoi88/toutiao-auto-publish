---
name: V1102.6 接续算法 bug 修法 (微头条 gtg_batch.py)
description: V1102.5 接续算法被 if _wl_q 包住,手动重启不走 catchup 时跳过接续 → V1102.6 移出 + sub_rounds 动态
type: reference
originSessionId: 65e7943b-4b50-4d8f-8d15-a85ca3997cff
---
V1102.5 mac gtg_batch.py 接续算法 bug + V1102.6 修法 (2026-05-09 NEO2 实证):

## V1102.5 设计 (双路径)
- 路径 A: 用户跑 catchup.py 写白名单 → gtg_batch 启动读白名单 → 进 if _wl_q 分支 → 接续算法跑
- 路径 B: 直接 gtg_batch.py 跑 (不走 catchup) → 白名单空 → 不进 if _wl_q → **接续算法被跳过** → 主循环从账号 1 全员重发

## V1102.5 漏洞 (line 2596-2616)
接续算法 (读 last_published.txt + 环形重排) 嵌套在 if _wl_q: 块内,只在路径 A 跑。

## NEO2 19:32 实证 (V1102.5 行为)
日志只有 done_in_round 推算 log,缺关键的"中断处自动接续"log → 算法没跑 → 全员从账号 1 重发。

## V1102.6 修法 (两 patch)
1. **接续算法移出 if _wl_q 块** (无论白名单是否存在都跑):
```python
if _wl_q:
    accounts = _new_accounts  # 只保留路径 A 重排
# ↓ 接续算法提到 try-except 外
_last_published_acc = ...读 last_published.txt 末位...
if _last_published_acc and accounts:
    # 找 idx + 环形重排 accounts[next:] + accounts[:next]
```
2. **sub_rounds 改为动态** (line ~2660):
```python
_max_quota = max(quota_map.values()) if quota_map else 5
result = run_death_grip(..., sub_rounds=_max_quota, ...)  # 不再写死 5
```

## NEO2 20:44 实证 (V1102.6 修后)
日志出 `[v1102.6] 中断处自动接续:最近 publish「半生轻狂客」(idx=88) → 从下一位「吧啦啦熊样」起跑` ✅

## 影响范围
5 机 × 3 大件 = 15 个文件 (微头条 gtg_batch + 文章 gtg_batch + 文章定时 gtg_timer 各 5 个);文章/文章定时也可能同款 if _wl_q 包接续,要查。

## 应用
- 重启发文中断后必须自动接续断点账号 + 完成本小轮 + 缺 N 补 N + 跑完所有 quota 小轮
- quota 不 cap 5 (微头条上限去掉);sub_rounds 必须 = quota 才能跑满
