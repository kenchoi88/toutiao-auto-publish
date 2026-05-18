---
name: reference-cdp
description: "罐头 = page+10webviews+2SW 嵌套结构, 真按钮在 webview 内 (757,487), gtg_batch.py 用屏幕坐标 (1547,593) 经\"罐头窗口 → WEBVIEW容器 → DPR\"投射. CDP WS 必 suppress_origin 绕 Chromium 117+ 403. _cdp_probe.py 是故障现场基线探针 (2026-05-18 新台机 4h 失败案立)"
metadata: 
  node_type: memory
  type: reference
  originSessionId: d42ef16d-8751-413e-8cd0-08a6b1f215d0
---

# 罐头 CDP 结构 (实证 2026-05-18, V1103 + 创作罐头 1.7.11.0)

罐头是 Electron app, CDP 9223 暴露 13 个 targets:

```
1 page         → 罐头主控台 (https://www.czgts.cn/v1/account/account)
                 viewport 1602x1152  DPR=1.5 (新台机 144 DPI 时)
10 webview     → 头条号 (mp.toutiao.com), 每登录账号 1 个
                 1 个活跃 = profile_v4/weitoutiao/publish  viewport 1386x1060 DPR=1.5
                 9 个待机 = profile_v4/index  viewport 0x0
2 service_worker
```

**关键**: 真按钮在 webview 内, 不在主控台. gtg_batch.py 第 459 行用 `czgts.cn` URL 找的是主控台 target, click 经过 win32 SetCursorPos 走屏幕坐标, 真命中目标在 webview 内坐标系.

## 坐标链 (屏幕 → webview 内)

```
屏幕物理坐标 (1547, 593)
  ↓  减 罐头窗口 client origin
罐头主控台逻辑坐标 ≈ (1547, 593)/DPR(1.5) = (1031, 395)
  ↓  命中 <WEBVIEW> 容器 (class webview-mXicTg webviewActive-pp_hGe)
  ↓  减 WEBVIEW 容器 rect.origin
webview 内逻辑坐标 ≈ (757, 487)  ← "文档导入" 按钮 79x27, 3 个重叠 DOM
  ↓  乘 DPR 1.5
webview 物理像素 (1136, 731)
```

**只有 罐头窗口位置 + WEBVIEW 容器位置 + DPR 三者全部不变, (1547,593) → 按钮(757,487) 才成立**. 任何一环偏 50px 即 click 投错 → "弹窗未出".

## CDP 连接 (绕 Chromium 117+ 403 Origin 拒绝)

```python
import websocket
WS_OPTS = {"suppress_origin": True}  # gtg_batch.py:46 同款
ws = websocket.create_connection(url, timeout=5, **WS_OPTS)
```

不加 suppress_origin → `Handshake status 403 Forbidden` + 提示 `--remote-allow-origins=*`. 我们不动罐头启动 flag, 客户端不发 Origin 头即可.

## 故障现场基线探针 _cdp_probe.py

位置: 本地仓库根 `_cdp_probe.py` + 新台机 `C:\Users\kench\_cdp_probe.py`
正常态基线 (新台机 5/18 21:00): `运行报告/20260518/baseline_snapshot_*.json` 共 4 份

抓取的字段 (每 webview/page):
- viewport.w/h, devicePixelRatio
- elementFromPoint(1547, 593) 命中 DOM (tag/cls/txt/rect/parents)
- 全部 `<webview>` 元素 getBoundingClientRect (主控台层关键中间变量)
- "文档/导入/上传" 按钮 rect 列表
- 全部 modal/overlay/mask/dialog/loading rect + covers_target=true/false
- 前台窗口 + 鼠标 + 进程列表

## 故障现场抓取 SOP (含 [[feedback_新台机微头条早晨连续失败排查SOP]] 的根因待证场景)

1. 缺哥发现失败 → **不要物理点**, 先喊
2. 跑探针 (~5s, 无侵入只读):
   ```
   ssh kench@100.95.244.10 'C:\Users\kench\AppData\Local\Programs\Python\Python312\python.exe C:\Users\kench\_cdp_probe.py'
   ```
3. 输出新 `baseline_snapshot_HHMMSS.json`, diff 跟正常基线:
   - 活跃 webview viewport / DPR 变没变?
   - "文档导入" 按钮 rect 偏了没?
   - WEBVIEW 容器在主控台坐标系 rect 偏了没? ← 最可能是这里
   - overlays 有没有新覆盖 (1547,593) 的层?
4. **再让缺哥物理点击**, 跑第 2 个 snapshot 拿 after state
5. before/after diff 锁根因

## 相关
- [[reference_新台机基础档案]] — 新台机 KENCHOIWINMINI 硬件 + profile
- [[feedback_2026_05_17_新台机搬家累积翻车]] — 新台机搬家过程的累积坑
- [[reference_4mac真版位置]] — 5 机 3 件素材路径全集
- 故障说明_2026-05-18.txt — 当日 4h 失败完整排查记录 (未修)
- gtg_batch.py:46 — `WS_OPTS = {"suppress_origin": True}` 原源
- gtg_batch.py:459 — `czgts.cn` URL 找主控台 target 原源
