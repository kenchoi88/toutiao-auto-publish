---
name: 程序网络慢/被代理绑架先查 env 三件套
description: Python 程序网络慢/被 v2rayN 绑架时, 先 echo HTTPS_PROXY / NO_PROXY / trust_env, 不要先动 v2rayN 配置, 也不要先怀疑目标服务/网络
type: feedback
originSessionId: 07bcf7db-9146-481d-9279-e63808562728
---
**症状**: Python 程序请求国内 API (volces/aliyun/baidu/腾讯云) 慢/超时, 但浏览器/curl 直接访问正常 → "被 V2 绑架"

**诊断三件套** (PowerShell 顺序跑):

```powershell
$env:HTTPS_PROXY        # 进程级 HTTPS 代理 (Python requests 读这个)
$env:HTTP_PROXY         # 同上 HTTP
$env:NO_PROXY           # bypass 域名列表(空 = 不 bypass)
(Get-ItemProperty 'HKCU:\Software\Microsoft\Windows\CurrentVersion\Internet Settings').ProxyOverride
```

**判定**: HTTPS_PROXY 有 v2rayN 地址 (`http://127.0.0.1:10808`) 且 NO_PROXY 空/不含目标域名 = 必中招。

**Why**:
- Python `requests` 库 `trust_env=True` (默认) 读 HTTPS_PROXY env, **不读** Windows 注册表 ProxyOverride
- Win 注册表 ProxyOverride 只对浏览器/IE/Edge/WinHTTP 类客户端生效
- v2rayN 启动时把 HTTPS_PROXY env 设为自己 → 所有 Python `requests` 默认全走 v2rayN → 国内 API 被转发到境外节点 = 慢/失败

**修法 (三层保险)**:

```python
# 层 1: 文件顶部清 env (新进程读不到)
import os
os.environ.pop('HTTP_PROXY', None)
os.environ.pop('HTTPS_PROXY', None)
os.environ.pop('http_proxy', None)
os.environ.pop('https_proxy', None)
os.environ['NO_PROXY'] = '*'  # bypass 所有域名

# 层 2: session 不读 env
session = requests.Session()
session.trust_env = False

# 层 3: 调用层显式 proxies=None (最高优先级,覆盖一切)
session.post(url, ..., proxies={'http': None, 'https': None})
```

**How to apply**:
- 遇 "程序慢/被代理绑架/V2 绑架" 第一反应 = 跑三件套 (不要先动 v2rayN, 不要先 kill V2 — 见 feedback_dont_kill_v2.md)
- 三件套 30 秒能查清, 比怀疑配置/网络/服务快 100 倍
- 改 v2rayN routing/ProxyOverride 对 Python `requests` 无效, 必须改代码

**反面教训**:
2026-05-11 我遇同类 bug 卡半天 (怀疑 v2rayN 配置/服务/网络), 缺哥骂半天没解决。
2026-05-12 缺哥提同样问题, 直接 grep `HTTPS_PROXY env` + `APIADDR` 两步定位根因 (ds_creator.py 用 `requests.post` + `HTTPS_PROXY=v2rayN` + APIADDR=火山北京区), 半小时上三层 patch + 重启洗稿。
