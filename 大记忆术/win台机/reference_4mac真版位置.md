---
name: 4 Mac 三大件真版位置(本地副本)
description: air/neo/neo2/mini 的三大件 gtg_*.py 都在桌面 ~/Desktop/<大件>/,4 台同款无差异(2026-05-03 实测)
type: reference
originSessionId: 6198d8da-e501-4a0b-b8de-45446700703e
---

## ⚠️ 2026-05-03 实测纠正

之前这条写"air+mini=`文章定时自动发布/`、neo+neo2=`Mac文章定时自动发布/`(带 Mac 前缀)"是**错的**,缺哥早就改成 4 台同款了。SSH 实测全 4 台 = `~/Desktop/文章定时自动发布/`,无 Mac 前缀,无 ~/code 路径。

## 速查 — 4 Mac 三大件真版位置(2026-05-03 实测)

**4 Mac 同款,全在桌面**:

```
~/Desktop/微头条自动发布/      gtg_batch.py + go.command
~/Desktop/文章自动发布/        gtg_batch.py + go.command
~/Desktop/文章定时自动发布/    gtg_timer.py + go.command + 定时发布.xlsx + 账号配置.xlsx
```

每个大件下还有:
- `素材/` — 待发 docx 池
- `素材/已发送/` — 历史归档
- `运行报告/<日期>/运行日志.txt`

## SSH 用户名(参 [reference_SSH用户名规律.md])

- air `kenair@100.67.252.1`
- neo `kenchoios@100.68.57.96`(1 个 i ⚠️)
- neo2 `kenchoineo2@100.96.153.17`
- mini `kenchoimini@100.70.22.7`

## 关键 xlsx(文章定时)

`~/Desktop/文章定时自动发布/`:
- `定时发布.xlsx` — B1 = 发布日期(每天改一次,改这格就好)
- `账号配置.xlsx` — 账号清单 + 配额
- `发文汇总.xlsx` — 历史汇总

## How to apply

- **不要再说"neo+neo2 用 Mac前缀"**,4 台都是 `文章定时自动发布/`
- 实际版本(v1101.X)看 grep 标记 + .bak 时间戳,本条只记位置
- 如果远程 SSH 进去找不到这些路径,先 `ls -d ~/Desktop/*` 实勘,再更新本文件
