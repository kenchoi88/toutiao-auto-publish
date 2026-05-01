---
name: 4 台 Mac 三大件真版位置(2026-05-01 22:?? 实证)
description: 各 Mac 桌面+仓库里"实际跑的脚本路径",别再每次 ssh 现查
type: reference
scope: 4-Macs (air/neo/neo2/mini)
verified_at: 2026-05-01 22:??
verified_by: 绣虎(Win 台机) 跨机 ssh + find + grep v1101 标记
---

> **生效:2026-05-01 实测一遍。下次再问 Mac 真版在哪,直接读这条,不要再 ssh 现找。**
> **谁记的:绣虎 — 缺哥要"别再问一遍"。**

## 微头条 + 文章件(4 台一致)

```
~/Desktop/微头条自动发布/gtg_batch.py
~/Desktop/文章自动发布/gtg_batch.py
```

4 台 Mac 都长这样,**桌面是真版**(跟 Win 台机同款"桌面才是真版"约定)。

## 文章定时件(命名分两派)

| 机器 | 路径 |
|------|------|
| **air** | `~/code/头条自动发布/文章定时自动发布/gtg_timer.py` |
| **mini** | `~/code/头条自动发布/文章定时自动发布/gtg_timer.py` |
| **neo** | `~/code/头条自动发布/Mac文章定时自动发布/gtg_timer.py` |
| **neo2** | `~/code/头条自动发布/Mac文章定时自动发布/gtg_timer.py` |

注意:
- air + mini = `文章定时自动发布/`(无 Mac 前缀)
- neo + neo2 = `Mac文章定时自动发布/`(带 Mac 前缀)
- 文章定时件**不在桌面**,而在仓库工作树内的目录里直接跑

## 各机桌面其它目录(供参考)

- **air**:`Desktop/{微头条,文章,Mac文章}自动发布/、文档分发/、阿良记忆/`
- **neo**:`Desktop/{微头条,文章}自动发布/、.ipynb_checkpoints/`
- **neo2**:`Desktop/{微头条,文章}自动发布/`
- **mini**:`Desktop/{微头条,文章,Mac文章}自动发布/、自动微头条素材/`

## SSH 用户名速查(重复但常用)

| 机器 | user@ip |
|------|------|
| air | `kenair@100.67.252.1` |
| neo | `kenchoios@100.68.57.96` |
| neo2 | `kenchoineo2@100.96.153.17` |
| mini | `kenchoimini@100.70.22.7` |

(完整规则见 `reference_SSH用户名规律.md` + `reference_Tailscale网络.md`)

## 改版同步落点(给绣虎做 Step 6 用)

跨机 v110X.Y patch 时:
- 微头条 + 文章件:`~/Desktop/{微头条,文章}自动发布/gtg_batch.py` 4 台路径一致
- 文章定时件:按上表分别处理 air/mini vs neo/neo2 命名差

## 注意:本条记的是位置,不是版本

- 实际跑哪个版本(v1101.3 / v1101.4 / ...) 看那个文件**头部 grep `v1101.X`** 或 **同目录 `.bak_pre_v1101.X_*`** 时间戳
- 命名"Mac文章定时自动发布"vs"文章定时自动发布"哪个 Claude 做的事 — 不是错乱,是各 Mac 历史命名差异;**统一改名风险大,别动**

## Mac 端 patch 时机(2026-05-01 缺哥追加)

**跑中可 patch,不必等任务停。**

- Python 进程已加载 .py 到内存,改文件不影响当前运行的进程
- patch 完后,**下次启动**脚本就是新版
- .pyc 缓存若担心,patch 时一并删 `__pycache__/` 即可
- 故 Step 6 跨 Mac patch 时,**不用 kill 跑中进程,不用问"能不能停"**,直接动手

## git ahead/behind 不一定是真漂移(2026-05-01 缺哥澄清)

跨机查 `git rev-list --count origin/main...HEAD` 看到 8/32/50/26 ahead,**不代表各机各自改了 8/32/50/26 个 commit**。

- 只有 **air 是本地真有改动**(阿良在妈家做了 hotfix)
- neo/neo2/mini 的 ahead 是**历史引用差异 + 早被推过又被各机本地保留的旧 commit**,不是漏推
- 看是否真漂移,**实证看桌面 .py 的 v1101.X 标记 + .bak 时间戳**,不靠 git ahead 数判
- Step 6 同步前不必"先解决各机 ahead",直接 patch 即可
