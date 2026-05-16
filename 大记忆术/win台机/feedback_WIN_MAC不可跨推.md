---
name: feedback-win-mac
description: "WIN 和 MAC 是两条独立线 (V1102.8 之后), 归档时严禁拿一边版本当另一边推 (绣虎 5/14 V1102.9 错推 win 到 mac 引连锁退化债)"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 6590fd21-264a-4cca-9599-9b4151b2ee6a
---

**红线**:WIN 台机版本 ≠ MAC 真版, 两条独立线, 严禁跨推。

**Why:**
2026-05-14 V1102.9 commit 时, 绣虎(我)误把 win 版 `gtg_batch.py` 拷贝到归档 `mac/` 目录, 推到 4 mac 后无法发文 (`X 异常: No module named 'win32gui'`), 缺哥发现叫停。后续修复 5/15-5/16 把 win 风格污染 (前缀模糊 + collect break 简化 + ZOOM_FIX_ACCOUNTS) 残留也带到 mac, 引出 +2 容器面板伪账号 / sent_accounts_set 跳接续点等一连串退化债, 累计 3 天补丁套补丁。

**WIN 和 MAC 的差异 (5/13 V1102.8 之后)**:
| 维度 | WIN 台机 | MAC (mini/air/neo/neo2) |
|---|---|---|
| 鼠标输入层 | win32api / win32gui / ctypes | cliclick (memory `feedback_真鼠标点击_勿换CDP` 红线) |
| 罐头 CDP 端口路径 | `%APPDATA%\创作罐头\DevToolsActivePort` | `~/Library/Application Support/创作罐头/DevToolsActivePort` |
| ACCOUNT_CLASS | "account-" 前缀模糊 + collect break 简化 (V1102.8 win 抗 hash 升级) | "account-cBAwuL" 精确 hash (V1103 写死, 罐头升级人工改 1 行) |
| ZOOM_FIX_ACCOUNTS | 有 (V1102.8 win 一笑酒暖花深修法) | 没有 |
| collect_accounts | B 方案 same_count 容错 + 兜底循环 (V1103) | V1102.7 mac 原版 has_scrolled + same_count >= 6 |

**How to apply:**
- 归档 V1XXX/<件>VXXX/ 时, mac/ 和 win/ 子目录**内容必须分开来源**:
  * mac/ ← 拉 mini 桌面真版 (`scp mini:~/Desktop/<件>/gtg_<batch|timer>.py`)
  * win/ ← 拉台机桌面真版 (`cp c:/Users/kench/Desktop/台机专用自动发布/<件>/`)
- 归档前必 grep 关键标记实证:
  * mac/ 必须 `win32 出现数 = 0`, `cliclick 出现数 >= 20`
  * win/ 必须 `win32api 出现`, `cliclick 出现数 = 0`
- 推前对比 mac/ vs win/ md5 — 必然不同 (相同 = 错推)
- 跨线移植算法改动 (比如 mac 接续算法 patch 也要推 win 台机) 必须**逐文件单独操作**, 不能 cp 整个 mac/ 到 win/

**关联:**
- V1103 版本说明: `自动发布/自动发布V1103/V1103版本说明.txt` 第二三节 mac/win 独有改动
- 故障说明 5/15 故障 1: `自动发布/故障说明/故障说明_2026-05-15.txt`
- 故障说明 5/16 故障 2: `自动发布/故障说明/故障说明_2026-05-16.txt`
- 红线 cliclick (mac): [[feedback_真鼠标点击_勿换CDP]]
- 红线 win 自杀 v2: [[feedback_dont_kill_v2]]
