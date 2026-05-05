---
name: 跨机协同作战分工 - 绣虎总指挥+现场机实操
description: 涉及多机/单机不能闭环的故障,绣虎(我)指挥+推理+裁判+立memory,现场机Claude本机实操拿root+实证;两边并行,缺哥拍板
type: feedback
originSessionId: 9d19d23b-db65-4712-96ac-91a7a3b3783b
---
# 跨机协同作战分工模式

(2026-05-05 缺哥拍立条,基于当晚 air Tailscale 走 SFO relay 跨 5h 闭环案例)

## 触发条件

任意一条命中即启用本分工:
- 故障跨多台机器(单机看不全)
- 操作需要 sudo/root 权限,绣虎 ssh 没本机密码
- 操作涉及实时人机交互(如 Tailscale 浏览器认证)
- 单台机的 daemon/launchd/系统配置改动
- 跨机配置矩阵审计(确认 4 mac/5 机一致)

不触发的场景: 单机本地故障/简单 ssh 一条命令能搞定的事 — 还是绣虎一手做。

## 角色分工

### 绣虎(Win 台机,我)
- **总指挥**: 判断方向 / 给方案 / 排序操作步骤
- **跨机协调**: ssh 进 mini/neo/neo2 做配置审计、灌 ssh 公钥、跨机文件分发
- **裁判 + 验证**: 现场机报输出后,客观判断方案是否达成、有无遗漏
- **立 memory + push**: 把今晚教训沉淀到 memory + 大记忆术 + git push,5 机共享

### 现场机 Claude(阿良 air / 小齐+小师弟 neo / 左右 neo2 / 东山 mini)
- **本机实操**: 跑 sudo / 改 launchd plist / 改 SQLite db / pkill 进程
- **现场实证**: 跑诊断命令拿一手输出
- **及时反馈**: 把 stdout / stderr / 关键状态文件内容贴给绣虎看
- **本机记忆**: 把本机特有的细节(plist 路径/db 字段/进程名)落到自己 memory 文件

### 缺哥
- **拍板**: 方案选项 / 是否动 / 范围(只动一台 vs 全员回灌) / 命名(版本号/hostname)
- **物理操作**: 浏览器认证 / WiFi 切换 / Web admin 后台改 / sudo 密码输入
- **复盘 + 沉淀指令**: 拍下"立 memory"或"丢弃,这事一次性"

## 协作节奏

```
缺哥提故障/需求
   ↓
绣虎 grep memory + 查仓库 + 推理 → 出方案 + 验证步骤(给到现场机的指令格式)
   ↓
现场机执行步骤 1 → 报输出
   ↓
绣虎裁判输出 → 给步骤 2(或调整方案)
   ↓
... (循环直到闭环)
   ↓
绣虎裁判方案达成 → 缺哥点头
   ↓
现场机更新本机 memory(实操细节)
绣虎更新跨机 memory(矩阵 + 沉淀经验) + push 仓库 + 同步大记忆术
```

## 关键 do/don't

- ✅ 现场机贴输出原文(不要总结),绣虎自己提取关键信息
- ✅ 绣虎给步骤要 quote 完整命令(避免现场机 quoting 出错)
- ✅ 双方都用一手实证,不靠"应该是"/"通常会"
- ✅ 步骤之间互相 sanity check,一方发现矛盾立刻暂停
- ❌ 现场机不要"自作主张优化方案",发现绣虎方案有问题先反馈
- ❌ 绣虎不要在现场机已经在跑的情况下连续追加新指令(等输出再下)
- ❌ 多 agent 同时改同一文件 — 绣虎指挥时明确"你改 A,我改 B"

## 实证案例

**2026-05-05 air 出街回家 Tailscale 走 SFO relay**:
- 故障: air 跟着缺哥连移动热点回 AX3,Tailscale fallback DERP relay,跨机 ssh RTT 370ms
- 绣虎诊断: 多个 tailscaled 进程并存 + Shadowrocket fake-DNS 劫 controlplane + skip-proxy 缺 100.64
- 阿良现场: 实测路由表 / 进程清理 / launchd plist HTTPS_PROXY 改 / db UPDATE / Rule 段 INSERT
- 跨机协调(绣虎): 灌 air pubkey 到 mini/neo/neo2 / 帮 neo 补 docid=2 / 验证 4 mac SSH 互信
- 闭环: 5h 跨机协作,4 mac 配置矩阵彻底统一,沉淀 3 条 memory(plist 修法 / db 三层 / 出门归来三查)
- 速度收益: 推 745 篇微头条 air 从 ETA 2h43m → 17s(SFO relay → direct)

## How to apply

- 收到跨机故障第一反应: 是不是要叫现场机协同? 单机搞不定别硬撑
- 现场机被叫起来后第一动作: grep 自己 memory + 发当前状态给绣虎(别上来就动手)
- 沉淀阶段不要省: 每次跨机调试都能挖出 1-3 条新 memory,跨机协作就是在修剪 memory 的"反向 grep"路径
