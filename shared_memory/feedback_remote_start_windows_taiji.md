---
name: 远程启动台机(Windows)脚本的前置条件 — 缺哥外出前必须做的"3 选 1"
description: Tailscale 通≠能远程启动脚本;Windows session 隔离 + Microsoft Account 双重锁住 SSH 跨 session 投递
type: feedback
---

# 远程操控台机踩的坑(2026-04-30 19:50 阿良在妈家实战折腾 30+ 分钟全失败)

## 事故概述

缺哥外出,台机微头条脚本 19:01 异常退出(差 62 篇没发到 320),阿良从 Air 经 Tailscale ssh 进台机
想远程双击 go.bat 重启 — **网络层全通但脚本死活起不来**,折腾半小时,62 篇报废,只能等缺哥回家手动双击。

## Why

Tailscale 给的是**网络层连通**,不是**进程跨 session 控制权**。Windows 远程启动 GUI 脚本被 3 件事卡死:

1. **Session 隔离**: SSH 进来落 session 0(无桌面),桌面 session 1 是缺哥本人在用。
   Session 0 起的 Python 戳不到 session 1 的鼠标/键盘/罐头窗口。

2. **跨 session 投递要本地账户密码**:
   - `schtasks /Create /RU /RP <密码>` → "用户名或密码错误"
   - PowerShell `Register-ScheduledTask -Password` → 注册后任务消失
   - `schtasks /IT` 不带密码 → Status=Running 但 Python 还在 session 0,UI 戳不到

3. **kench 是 Microsoft Account**(`PrincipalSource: MicrosoftAccount`):
   - 密码走 Hello/PIN/微软服务器验证,**本地 SAM 库里不存密码**
   - 任何本地密码(geng7997 / keneunice0816)schtasks 全拒
   - OpenSSH 能登只是因为它走 LSA cache 等其他认证路径,绕过本地密码校验

PsExec(SysInternals)未装,无法走 `PsExec -i 1 -d <bat>` 直接投递 session 1。

## How to apply

### 缺哥下次外出前必须做"3 选 1"(本机操作一次,5 分钟搞定)

1. **A 方案: 装 PsExec**
   - 下载 PsExec.exe 放 `C:\Tools\PsExec.exe`
   - 远程 SSH 进去后 `PsExec.exe -i 1 -d -accepteula C:\path\to\go.bat` 即可投递 session 1
   - 不需要密码

2. **B 方案: 任务计划程序"用户登录时触发"**
   - 提前在桌面 session 创建任务,触发器 = "用户登录时"
   - 远程 SSH 进去 `schtasks /Run /TN <task>` 拉一次,任务以 session 1 上下文跑

3. **C 方案: 向日葵 / AnyDesk unattended 模式**
   - 提前开启免确认远程
   - 外出后从手机/Air 直接连进桌面,人肉双击 go.bat

### Agent 接到"远程启动台机脚本"任务时

- **第一句话先查**:本机有没有 PsExec / 登录触发任务 / 向日葵 — 三个都没有就**直接告诉缺哥放弃**,
  开始浪费时间折腾 schtasks/PowerShell 之前先报警
- 不要再走 `schtasks /Create /RU kench /RP <password>` 这条死路 — Microsoft Account 注定拒
- Tailscale 通了只意味着 SSH 通了,**不意味着能远程启动 GUI 脚本**,这两件事别混

## 教训(写给所有 agent)

阿良 04-30 折腾 30+ 分钟全部失败,62 篇报废。**根因不是技术不会,是缺哥外出前没装前置工具**。
所以 agent 当下能做的是:**在缺哥下次外出前主动提醒装 PsExec / 配登录触发 task / 开向日葵**,
不要等下次外出脚本崩了又一次现场抓瞎。
