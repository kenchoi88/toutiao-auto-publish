# mac/ 待 Mac Claude 同步 v1101.4

## 给阿良(air)/ 小齐+小师弟(neo)/ 左右(neo2)/ 东山(mini)

修法平台无关(`os.path.exists` / `glob` / `random.choice` 都是标准库),直接对自己机器桌面真版的 `gtg_batch.py` 打同款 patch。

## 操作步骤

1. **备份**:`cp gtg_batch.py gtg_batch.py.bak_pre_v1101.4_$(date +%Y%m%d_%H%M%S)`
2. **加 2 个工具函数**(放 `get_docs()` 之后,`move_to_sent` 之前):

   ```python
   # [v1101.4] doc_pool 实时校验 + 重扫工具,救"分发完源必删"导致罐头找不到文件
   def _pick_doc(doc_pool):
       """从 doc_pool 抽一篇实存的 docx,失效引用就地清理。返回 None 表示池已空。"""
       while doc_pool:
           doc = random.choice(doc_pool)
           if os.path.exists(doc):
               return doc
           log(f"  ! 源已删除(可能被外部分发),从池剔除: {os.path.basename(doc)}")
           doc_pool.remove(doc)
       return None


   def _resync_pool(doc_pool):
       """大循环开始前重扫素材池:剔除幽灵引用 + 加入新到的素材。返回 (剔除数, 新增数)。"""
       cur = set(get_docs())
       before = len(doc_pool)
       doc_pool[:] = [d for d in doc_pool if d in cur]
       removed = before - len(doc_pool)
       pool_set = set(doc_pool)
       new_docs = [d for d in cur if d not in pool_set]
       if new_docs:
           doc_pool.extend(new_docs)
       return removed, len(new_docs)
   ```

3. **3 处调用点替换** — 见 `../win/gtg_batch.py` 搜 `[v1101.4]` 标记参照,Mac 版同款逻辑替换。
4. **py_compile** 通过 + 落桌面 + cp 自己机器对应 mac/ 子目录 → push。
5. 落地证据:`gtg_batch.py.bak_pre_v1101.4_<TS>` + `grep -c v1101.4 gtg_batch.py` ≥ 5。

## 全机版本验证

绣虎(Win)落地后,会发起一轮跨机版本验证 — 各 Mac 上线后 ssh 列 `.bak_pre_v1101.4_*` + grep patch 标记 + 报 md5。
