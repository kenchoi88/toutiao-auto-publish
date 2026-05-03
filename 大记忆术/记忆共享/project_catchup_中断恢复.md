---
name: 中断恢复一键 catchup.py — 缺 N 补 N(2026-05-02 凌晨断网事件后立)
description: 三大件中断后,启动 catchup.py 自动算漏数 + 环形排序写白名单,启动 go.command 即续
type: project
scope: 微头条 / 文章 / 文章定时(三大件)
effective: 2026-05-02
---

> **诞生于 2026-05-02 04:09 电信断网事件**(全队 Stage 1 中断,误判硬终止 394 个账号)。
> 缺哥拍板:**沉淀成一键工具,以后任何件中断,3 步搞定**。

## 触发场景

任一件中断:
- **文章定时件**(gtg_timer.py)— 凌晨断网那种,Stage 1 排程到一半挂
- **微头条 / 文章自动发布**(gtg_batch.py)— 主动 Ctrl+C / 罐头死 / 网抖

## catchup.py 干 4 件事

### 1. 找断点
- 读最新 log(运行报告/<最新>/运行日志.txt,按 mtime)
- 抽 **最后一篇 ✓ 发文成功 / ✓ 定时发布成功** 的账号 → 它是"断点的前一个"
- 当前在第几大循环 / 第几小轮(从 log 里 `第 X 大循环 / 第 Y 小轮` 标记拿)

### 2. 算漏数(缺 N 补 N)
**优先级**:
1. 文章定时件「待补漏」sheet(脚本自己写的,权威)
2. log 里 quota - 累计成功 = 漏数

**关键**:1 小轮内未发成功的账号都算待补(失败 + 没跑到 都算)。

### 3. 环形重排
- 断点账号(最后成功的下一个)→ 第一位
- 顺序到末尾 → 绕回开头
- 用 Python 一行:`ordered = items[idx:] + items[:idx]`

### 4. 写白名单
- 备份 `账号配置.xlsx.bak_catchup_<TS>`
- 清空原白名单,写入 N 行(账号名 + quota=漏数)
- 报告:断点账号 / 大循环 / 小轮 / 待补总数

## 件类型适配

| 件 | 小轮数 | 路径 |
|---|---|---|
| 微头条自动发布 | 5 | ~/Desktop/微头条自动发布/catchup.py |
| 文章自动发布 | 3 | ~/Desktop/文章自动发布/catchup.py |
| 文章定时(中断恢复)| 3(死磕)| 通过 文章自动发布/catchup.py 读「待补漏」补 |

文章定时件中断后,直接走 文章自动发布 catchup.py(立即发模式补漏)— 不需要单独脚本。

## 配套:gtg_batch.py 必须按 xlsx 顺序跑(v1101.5 hotfix)

原 gtg_batch.py 按罐头侧边栏顺序跑 → xlsx 重排无效。
v1101.5 hotfix:在 _wl_map 加载后按白名单 keys 顺序重排 accounts。
**catchup.py 只在 v1101.5+ 的 gtg_batch.py 上才生效**。

## 用户操作(中断后,3 步)

```bash
cd ~/Desktop/<件>自动发布
python3 catchup.py        # 一行,看输出
双击 go.command           # 启动跑
```

## 部署

5 机各自的:
- mini / air / neo / neo2:`~/Desktop/{微头条,文章}自动发布/catchup.py`
- Win 台机:`~/Desktop/台机专用自动发布/{微头条,文章}自动发布/catchup.py`

## Why

- 凌晨电信断 → 全队 4 Mac Stage 1 中断 → 误判硬终止 394 个账号 → 手动补漏耗 1 小时
- 沉淀成 catchup.py = 下次同款情况 30 秒搞定
- 「待补漏」sheet 是脚本自己已记的,数据权威 — catchup.py 只是消费

## 关联规则

- feedback_发文上限与补漏规则.md(漏 N 补 N)
- feedback_文稿分发只存一.md(分发完源必删)
- project_定时发布两阶段.md(Stage 1/2 架构)
- v1101.x 待修缺陷攒清单 ①(mac/gtg_timer.py 中断恢复 — 这是另一面,gtg_timer 自身的中断恢复需大版本改)
