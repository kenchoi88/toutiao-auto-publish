---
name: 头条号内容数据定时导出
description: 每天23:50自动从头条API拉当月累计数据，写Excel统计表，launchd已配置完成
type: project
originSessionId: 6d1e89eb-eddc-422c-b35c-b420271a3a68
---
## 已完成（2026-04-11）

**核心发现：完全不需要罐头开着**
- cookie存在磁盘SQLite文件里，直接读，不走CDP
- 母账号（青春小馆）Partition：`7477169161966321683`
- 主Cookie文件：`~/Library/Application Support/创作罐头/Cookies`
- Partition Cookie：`~/Library/Application Support/创作罐头/Partitions/7477169161966321683/Cookies`
- 两个文件都读，合并cookie，母账号sessionid在Partition文件里

**头条内容管理API：**
- 文章：`https://mp.toutiao.com/mp/agw/media_matrix/list?type=1&size=50&page_num=N&from=日期&to=日期&app_id=1231`
- 微头条：同上，`type=3`
- 需要分页翻取（每页50条，11号文章393条=8页，微头条679条=14页）
- 返回字段：`article_attr.title/nick_name/create_time` + `article_stat.impression_count(推荐量)/go_detail_count(阅读量)`

**脚本：** `~/小馆数据/data_export.py`（2026-04-14从Desktop移到Home，修复launchd权限问题）

**Excel输出：** `~/小馆数据/小馆YYYY年MM月数据.xlsx`
- 每行一天，列分四组：微头条快照 / 文章快照 / 微头条24h增量 / 文章24h增量
- 快照字段：发文数、总阅读量、(文章有)总推荐量、0阅读/1k-5k/5k-1w/1w+各账号数
- 增量 = 本次快照 - 上次快照（昨天存的JSON）
- 第一次跑无增量（无历史快照），从第二天起有增量

**快照JSON：** `~/小馆数据/snapshot_YYYYMM.json`
- 每次运行结束后覆盖写入
- 格式：`{day_str: {micro: {total,read,dist:[0阅,1k-5k,5k-1w,1w+]}, article: {total,read,recommend,dist}}}`

**launchd：** `~/Library/LaunchAgents/com.xiaoguan.dataexport.plist`
- 每天23:50触发，已load
- 日志：`~/小馆数据/export.log`

**运行逻辑：**
1. 读磁盘cookie（主+Partition）
2. 加载上次快照（prev_snapshot）
3. 循环本月1号到今天，每天分别拉文章+微头条（自动翻页）
4. 计算当前数据 vs 上次快照的差值（24h增量）
5. 写Excel（月初到今天，每行一天）
6. 覆盖保存今天快照

**Why:** 头条后台有现成API，cookie从罐头磁盘文件读，全程不依赖UI和罐头进程，定时任务完全自动。
**How to apply:** 脚本和launchd已部署在Air（阿良这边），不在mini。如cookie过期（sessionid失效），需要重新打开罐头让它刷新cookie，再跑一次即可。月底跨月时自动切换新Excel文件，旧月数据保留。

**注意（2026-04-13）：** 发文任务已迁移到mini（崔东山），但数据导出任务继续留在Air，不要动。
