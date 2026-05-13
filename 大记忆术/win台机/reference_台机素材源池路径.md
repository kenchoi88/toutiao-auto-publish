---
name: ""
description: "台机两个素材源池根目录(微头条 / 文章),分发给 5 机的源在这里"
metadata: 
  node_type: memory
  type: reference
  originSessionId: a4ef6977-8047-4e85-a5e0-0eb33eb7c363
---

## 源池根路径(2026-05-13 缺哥拍 — 每天用,不再问)

| 类型 | 根路径 | 内含 |
|---|---|---|
| **台机头条源(微头条池)** | `C:\Users\kench\Desktop\台机DS创作微头条\` | `<日期-时间-N篇>\` 子目录,每天新建一个时间戳目录,内有 docx |
| **台机文章源(文章池,自动+定时共用)** | `C:\Users\kench\Desktop\台机DS创作新文章\` | 同上 |

## 怎么找"今天的源"

每天新建的子目录形如:`2026年05月13日-18时27分46秒-2069篇`(目录名末尾的"N 篇"是导出时罐头总数,**不是 docx 实际数**,要 ls 实际计)。

找最新子目录的 bash 一行:
```bash
ls -td "/c/Users/kench/Desktop/台机DS创作新文章/"*/ | head -1
```

或 Python:
```python
from pathlib import Path
roots = [p for p in Path("C:/Users/kench/Desktop/台机DS创作新文章").iterdir() if p.is_dir()]
latest = max(roots, key=lambda p: p.stat().st_mtime)
```

## 分发后规矩 — 推完源删

按 [[feedback_文稿分发只存一]]:推到 5 机后,**台机源池删那批 docx**(scp 是 cp 不删源,要主动 rm),目标池别加 2 次同源 doc,跨机标题查重防类同扣分。

## 与目标的对照

目标素材路径见 [[reference_4mac真版位置]] 的「写死路径全集」表(5 机 × 三大件 素材目录)。

源 → 目标 关系:
- 台机头条源(微头条池) → 5 机微头条自动发布/素材/
- 台机文章源(文章池) → 5 机文章自动发布/素材/ + 5 机文章定时自动发布/素材/(同源切两批)
