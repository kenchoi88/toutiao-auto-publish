---
name: 4 Mac 三大件真版位置(本地副本)
description: air/neo/neo2/mini 的三大件 gtg_*.py 都在桌面 ~/Desktop/<大件>/,4 台同款无差异(2026-05-03 实测)
type: reference
originSessionId: 6198d8da-e501-4a0b-b8de-45446700703e
---

## ⚠️ 2026-05-03 实测纠正

之前这条写"air+mini=`文章定时自动发布/`、neo+neo2=`Mac文章定时自动发布/`(带 Mac 前缀)"是**错的**,缺哥早就改成 4 台同款了。SSH 实测全 4 台 = `~/Desktop/文章定时自动发布/`,无 Mac 前缀,无 ~/code 路径。

## 速查 — 4 Mac 三大件真版位置(2026-05-03 实测,2026-05-06 加口语映射)

**4 Mac 同款 + 台机同款,全在桌面**:

```
缺哥口语 (固定 3 词)  → 实际目录                       三大件 / 关键 xlsx
─────────────────────────────────────────────────────────────────────
「自动头条」          → ~/Desktop/微头条自动发布/      gtg_batch.py
「自动文章」          → ~/Desktop/文章自动发布/        gtg_batch.py
「定时文章」          → ~/Desktop/文章定时自动发布/    gtg_timer.py
                                                       + 定时发布.xlsx (B1=日期)
                                                       + 账号配置.xlsx
```

⚠️ **缺哥不说"微头条""文章""文章定时"**,固定 3 词。听到"自动头条"=微头条大件,"自动文章"=文章大件,"定时文章"=文章定时大件,秒映射目录,不再问路径。

**台机路径前缀**: 台机所有大件挂在 `C:\Users\kench\Desktop\台机专用自动发布\<大件>/`(就一层"台机专用自动发布"后续同结构)
**4 Mac 路径前缀**: 4 Mac 直接 `~/Desktop/<大件>/`(无 Mac 前缀,无嵌套)

每个大件下还有:
- `素材/` — 待发 docx 池
- `素材/已发送/` — 历史归档
- `运行报告/<日期>/运行日志.txt`

## SSH 用户名(参 [reference_SSH用户名规律.md])

- air `kenair@100.126.82.58`(2026-05-06 漂自旧 100.67.252.1)
- neo `kenchoios@100.68.57.96`(1 个 i ⚠️)
- neo2 `kenchoineo2@100.96.153.17`
- mini `kenchoimini@100.70.22.7`

## ⚠️ 写死路径全集 — 5 机 × 三大件 素材目录(2026-05-13 缺哥拍,不再问路径)

| 机 | 自动头条(微头条) 素材 | 自动文章(文章) 素材 | 定时文章 素材 |
|---|---|---|---|
| **台机** | `C:\Users\kench\Desktop\台机专用自动发布\微头条自动发布\素材\` | `C:\Users\kench\Desktop\台机专用自动发布\文章自动发布\素材\` | `C:\Users\kench\Desktop\台机专用自动发布\文章定时自动发布\素材\` |
| **air** | `/Users/kenair/Desktop/微头条自动发布/素材/` | `/Users/kenair/Desktop/文章自动发布/素材/` | `/Users/kenair/Desktop/文章定时自动发布/素材/` |
| **neo** | `/Users/kenchoios/Desktop/微头条自动发布/素材/` | `/Users/kenchoios/Desktop/文章自动发布/素材/` | `/Users/kenchoios/Desktop/文章定时自动发布/素材/` |
| **neo2** | `/Users/kenchoineo2/Desktop/微头条自动发布/素材/` | `/Users/kenchoineo2/Desktop/文章自动发布/素材/` | `/Users/kenchoineo2/Desktop/文章定时自动发布/素材/` |
| **mini** | `/Users/kenchoimini/Desktop/微头条自动发布/素材/` | `/Users/kenchoimini/Desktop/文章自动发布/素材/` | `/Users/kenchoimini/Desktop/文章定时自动发布/素材/` |

- 4 mac 用 ssh 时 `~` 自动展开成 `/Users/<用户>/`,Bash inline 单引号 `'ls ~/Desktop/...'` OK
- 子结构(每件素材目录下):`<docx 直接放>` + `已发送/`(历史归档) + `临时/`(发文中中转,通常空)
- 查"在不在发文" 看 `<件目录>/素材/*.docx` 直接的数(不含 子目录),不是 `已发送/`
- 查实际跑哪个件用 `lsof -p <pid> | grep cwd`,**进程名 gtg_batch.py / gtg_timer.py 不代表件**:文章定时件唯一脚本是 `gtg_timer.py`,微头条/文章自动用 `gtg_batch.py`

## 关键 xlsx(文章定时)

**⚠️ 文件名台机跟 mac 不一样,B1 字段同款**(2026-05-13 实勘):

| 机 | 文件路径 | B1 字段 |
|---|---|---|
| **台机** | `C:\Users\kench\Desktop\台机专用自动发布\文章定时自动发布\定时配置.xlsx` | `datetime(YYYY,M,D,0,0)` 发布日期 |
| **4 mac** | `~/Desktop/文章定时自动发布/定时发布.xlsx` | 同款 |

每件下:
- 上述定日期 xlsx — B1 改日期(每天改一次,sheet 名 = 文件主名)
- `账号配置.xlsx` — 账号清单 + 配额(用户手填,脚本只读 见 [[project_账号配置sheet_权属]])
- `发文汇总.xlsx` — 历史汇总(mini 无此文件)

## How to apply

- **不要再说"neo+neo2 用 Mac前缀"**,4 台都是 `文章定时自动发布/`
- 实际版本(v1101.X)看 grep 标记 + .bak 时间戳,本条只记位置
- 如果远程 SSH 进去找不到这些路径,先 `ls -d ~/Desktop/*` 实勘,再更新本文件
