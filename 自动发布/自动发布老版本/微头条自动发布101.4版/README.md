# 微头条自动发布 v1101.4

## 修了哪些 BUG

**doc_pool 启动快照与外部 mutate 冲突** — 「分发完源必删」规则下,scp 分发后 rm 源会让 doc_pool 里残留幽灵引用,脚本继续把不存在的路径塞进罐头「文档导入」对话框,导致罐头弹"找不到文件"。

详见仓库 `故障日志.txt` 「2026-05-01 22:00 台机三大件」段 + `版本说明.txt` v1101.4 段。

## 修法(3 个工具函数 + 4 处调用替换)

- `_pick_doc(doc_pool)` — 替代 `random.choice`,校验存在 + 失效就地剔除
- `_resync_pool(doc_pool)` — 大循环开头重扫,实时同步外部 mutate
- 4 处调用点替换:Phase A、Phase B 原 doc 路径校验、Phase B fallback、大循环 banner 之前

## 落地状态

- ✓ Win 桌面真版(`~/Desktop/台机专用自动发布/微头条自动发布/gtg_batch.py`)
- ✓ 仓库 `自动发布/微头条自动发布101.4版/win/gtg_batch.py`
- ☐ Mac 三大件(各 Mac Claude 拉仓库后自落,见 `mac/README.md`)

## 架构红线(本版坚决不动)

- Stage 1 / Stage 2 两阶段架构
- 篇间等待 8-20s sleep
- cliclick / win32api 真鼠标点击
- move_to_sent 语义
