---
name: 文档分发脚本
description: 台机→Air中转→4台Mac的docx文档分发方案，脚本已部署在Air桌面
type: project
originSessionId: 03181edf-0b59-4561-ab9a-c73bcb65d019
---
## 方案

台机桌面按机器分好文件夹，Air上跑脚本拉取并推送到各Mac。

**Why:** U盘传文档到mini很慢（macOS 26.3的exFAT小文件写入bug），局域网分发更快。

**How to apply:** 遇到分发/推送文档需求，直接用这套脚本，不用U盘。

## 台机文件夹结构（桌面）

```
台机DS创作微头条/
  air/ mini/ neo/ neo2/

台机DS创作新文章/
  air/ mini/ neo/ neo2/
```

## 各Mac目标路径

| 机器 | 微头条 | 文章 |
|------|--------|------|
| air | ~/Desktop/Mac微头条自动发布/素材/ | ~/Desktop/Mac文章自动发布/素材/ |
| mini | 同上（用户kenchoimini） | 同上 |
| neo | 同上（用户kenchoios） | 同上 |
| neo2 | 同上（用户kenchoineo2） | 同上 |

## 脚本位置

Air桌面：`~/Desktop/文档分发/dispatch.py`，双击 `go.command` 运行。

## 注意事项

- neo的IP不固定，现在写死192.168.10.243，变了要改dispatch.py里的host
- neo2的IP同样不固定，现在是192.168.10.245
- mini的IP：192.168.10.244（IP会变动，每次推前确认）
- Windows笔电已没了，现在局域网5台：台机(Win)、Air、mini、neo、neo2
- mini系统是macOS 26.3（比Air的26.4.1旧），需要更新才能解决U盘慢的问题
