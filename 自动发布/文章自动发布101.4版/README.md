# 文章自动发布 v1101.4

## 修了哪些 BUG

跟微头条 v1101.4 同款:doc_pool 启动快照与外部 mutate 冲突。详见 `自动发布/微头条自动发布101.4版/README.md`。

## 修法

3 个工具函数 + 4 处调用替换 — 跟微头条 gtg_batch.py 完全同款 patch(两件 batch 结构本来就一样,只 publish_article 内部不同)。

## 落地状态

- ✓ Win 桌面真版(`~/Desktop/台机专用自动发布/文章自动发布/gtg_batch.py`)
- ✓ 仓库 `自动发布/文章自动发布101.4版/win/gtg_batch.py`
- ☐ Mac 三大件(各 Mac Claude 拉仓库后自落,见 `mac/README.md`)
