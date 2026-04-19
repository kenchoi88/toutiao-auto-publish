---
name: 优先找API，不要上来就模拟UI
description: 遇到需要从网页抓数据的任务，先用CDP监听网络请求找到API接口，比模拟点击稳定得多
type: feedback
originSessionId: 6d1e89eb-eddc-422c-b35c-b420271a3a68
---
遇到需要从网页抓数据的任务，第一步是用CDP的Network.enable监听页面的API请求，找到真实接口URL，然后直接用requests带cookie请求，不要上来就模拟鼠标点击UI。

**Why:** 2026-04-11头条内容数据导出任务，最初方案是模拟点击导出Excel→保存对话框→重命名，卡在日历选日期这一步很久。后来改为监听API，发现 `mp.toutiao.com/mp/agw/media_matrix/list` 接口，直接请求拿JSON，彻底绕开UI，而且cookie可以从罐头磁盘SQLite直接读，连罐头进程都不需要开。

**How to apply:** 凡是Electron应用（罐头）或浏览器里的数据，优先CDP Network监听找接口，找到后直接requests请求。cookie优先从磁盘SQLite读（`~/Library/Application Support/<应用>/Cookies` 和 Partitions子目录）。
