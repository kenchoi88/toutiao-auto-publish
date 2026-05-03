---
name: 头条数据自动拉取方案（已跑通）
description: 小馆+迦境文章/微头条/收益自动拉取，每天必须跑一次，漏跑那天的列永久丢失
type: project
originSessionId: 4d54a0ae-a6c6-4a9f-8876-108bfe0c235c
---
## 脚本位置
`~/Desktop/MCN数据/data_pull.py`，目标文件 `~/Desktop/MCN数据/流量对比汇总.xlsx`

## 运行方式
- 正常：`python3 data_pull.py`（统计日=今天，补昨天发布日一行 + 今天统计列）
- 补跑：`python3 data_pull.py 2026-04-18`（指定统计日）

## 表结构（关键——看代码看不出）
- **文章/微头条 sheet**：行=发布日（4月2号…4月18号），列=统计日（15号推荐、15号阅读、16号推荐…）。每次运行**新增一列**，代表"今天去查每个发布日累计到今天的推荐/阅读"
- **收益 sheet**：行=每天，列固定（发文量/推荐量/阅读量/流转收益）。每次运行**新增一行**

## 接口
- 文章/微头条：`mp/agw/media_matrix/export?from=DATE&to=DATE&type=1|3&page_num=N&size=1000`（type=1文章/3微头条，翻页到<1000为止）
- 收益：`mp/agw/statistic/matrix/matrix_media_daily_stat_export?start_date=YYYYMMDD&end_date=YYYYMMDD&pagenum=N&pagesize=50`
- 收益xlsx列：`[头条号, 粉丝量, 粉丝新增, 发文量, 推荐量, 阅读量, 粉丝阅读, 播放量, 粉丝播放, 评论量, 收益, 流转收益, 粉丝收益]`

## Cookie
- 小馆：SQLite读 `~/Library/Application Support/创作罐头/Cookies` + `Partitions/7477169161966321683/Cookies`
- 迦境：CDP连罐头，优先 `matrix_manage` URL 的 webview。端口动态，读 `DevToolsActivePort` 文件

## 头条API两个大坑
1. **微头条xlsx只有3列**，阅读量在 `row[2]`，没有推荐量列（文章是4列：推荐 row[2]、阅读 row[3]）
2. **"当天"数据不可信**：当天查 `start_date=end_date=今天` 时，推荐量/阅读量字段会复用前一天的值（只有发文量是真的）。所以收益循环必须 `d < stat_date`，只拉到昨天为止

## 漏跑代价
**每天必须跑一次**。漏跑某天 → 那天对应的"统计列"永久丢失，因为头条不支持回查历史快照（只能查"截止到当前"的累计数）。缺哥 18 号漏跑后，19 号凌晨补跑勉强能用 18 号作为统计日，但越迟补越不准

**Why:** 替代手动每天从头条后台下载一堆xlsx。2026-04-19 完整跑通含收益API
**How to apply:** 建议加 launchd 每晚定时跑；迦境需罐头开着且有 matrix_manage 标签页
