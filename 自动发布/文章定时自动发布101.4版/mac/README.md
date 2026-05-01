# mac/ 待 Mac Claude 同步 v1101.4(文章定时件)

文章定时由两件 .py 协作:

## gtg_batch.py(死磕循环,Stage 2 用)

跟微头条/文章件 v1101.4 完全同款 patch — 详细工具函数代码 + 步骤见:

→ `自动发布/微头条自动发布101.4版/mac/README.md`

## gtg_timer.py(Stage 1 排程,文章定时独有)

加一个 `_pop_doc()` 工具函数(顺序取 + 校验存在),放 `get_docs()` 之后:

```python
# [v1101.4] doc_pool 顺序取 + 校验,救"分发完源必删"导致罐头找不到文件
def _pop_doc(doc_pool):
    """从 doc_pool 顺序取一篇实存的 docx,失效引用就地剔除。返回 None 表示池已空。"""
    while doc_pool:
        doc = doc_pool.pop(0)
        if os.path.exists(doc):
            return doc
        log(f"  ! 源已删除(可能被外部分发),跳过: {os.path.basename(doc)}")
    return None
```

调用点改 1 处(原 `doc_path = doc_pool.pop(0)`),改成:

```python
# [v1101.4] _pop_doc 替代 doc_pool.pop(0): 校验存在 + 失效就地剔除
doc_path = _pop_doc(doc_pool)
if doc_path is None:
    log("  X 素材池已空(全失效)")
    fail_records.append((datetime.now().strftime("%Y-%m-%d %H:%M"), name, timer_time, "", "素材不足"))
    fail_docs_by_acct.setdefault(name, []).append("")
    continue
log(f"  文档: {os.path.basename(doc_path)}")
```

参照 `../win/gtg_timer.py` 搜 `[v1101.4]` 标记。
