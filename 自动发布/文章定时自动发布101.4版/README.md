# 文章定时自动发布 v1101.4

## 修了哪些 BUG

跟微头条 v1101.4 同款:doc_pool 启动快照与外部 mutate 冲突。

文章定时由两件 .py 协作:
- `gtg_timer.py` — Stage 1 定时排程(顺序 `pop(0)` 取 doc)
- `gtg_batch.py` — Stage 2 死磕循环(随机 `random.choice` 取 doc,跟两件 batch 同源)

## 修法

- `gtg_timer.py`:加 `_pop_doc()` 工具函数(顺序取 + 校验存在 + 失效就地剔除),Stage 1 调用点 1 处替换
- `gtg_batch.py`:跟微头条/文章 gtg_batch.py 完全同款 patch(3 个工具函数 + 4 处调用替换)

## 落地状态

- ✓ Win 桌面真版(`~/Desktop/台机专用自动发布/文章定时自动发布/{gtg_timer,gtg_batch}.py`)
- ✓ 仓库 `自动发布/文章定时自动发布101.4版/win/{gtg_timer,gtg_batch}.py`
- ☐ Mac 三大件(各 Mac Claude 拉仓库后自落,见 `mac/README.md`)
