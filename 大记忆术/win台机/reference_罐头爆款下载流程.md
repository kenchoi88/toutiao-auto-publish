---
name: 罐头爆款下载流程(本地副本)
description: 触发词"下载爆款"=Win 台机跑 罐头爆款下载.py;前提罐头 CDP 9223 在线
type: reference
originSessionId: 6198d8da-e501-4a0b-b8de-45446700703e
---
真版在 `c:\Users\kench\code\头条自动发布\shared_memory\reference_罐头爆款下载流程.md`。

**触发词**:缺哥说**「下载爆款」/「下载爆款数据」** → 直接跑,不再问。

**前置**:罐头 CDP 9223 在线(报错时让缺哥双击 `~/Desktop/台机专用自动发布/<件>/debug_launch.bat`)。

**跑**:`cd C:/Users/kench/Desktop/罐头爆款下载 && python 罐头爆款下载.py`

**固化参数**:今日头条 / 短图文 / 2 天内 / 阅读量排 / 19 领域(见真版)

**领域改动史**:2026-04-29 删「科学科技」/ 2026-05-02 删「法律」加「综艺」

**输出**:`罐头爆款_<日期>/罐头爆款_<日期>_<时分秒>{,_原始,_urls.txt}.xlsx`

详见仓库真版。
