# -*- coding: utf-8 -*-
"""v1102.1 + v1102.2 — Mac 文章 batch.py 专用 patch"""
import sys, os
if len(sys.argv) < 2:
    print("用法: python script.py <文章/gtg_batch.py>"); sys.exit(1)
fp = sys.argv[1]
with open(fp, encoding='utf-8') as f:
    text = f.read()

if 'LAST_PUBLISHED_FILE' in text and '_last_published_acc' in text:
    print(f'  [{fp}] 已 patched, 跳过'); sys.exit(0)

errors = []

# step 1: 全局 LAST_PUBLISHED_FILE = None(在 NOTICE_CHECKED_FILE = None 后面)
old1 = 'NOTICE_CHECKED_FILE = None  # [v1102] 持久化已检查账号集合(中断恢复后仍只读 1 次)'
new1 = '''NOTICE_CHECKED_FILE = None  # [v1102] 持久化已检查账号集合(中断恢复后仍只读 1 次)
LAST_PUBLISHED_FILE = None  # [v1102.2] 持久化最近 publish 成功账号(中断恢复后从此账号下一位起跑)'''
if old1 in text: text = text.replace(old1, new1, 1)
else: errors.append('step1')

# step 2: _init_run_dir global 加 LAST_PUBLISHED_FILE
old2 = 'global LOG_FILE, FAIL_FILE, NOTICE_FILE, NOTICE_CHECKED_FILE, ALERT_FILE, VIOLATION_FILE, RUN_REPORT_DIR'
new2 = 'global LOG_FILE, FAIL_FILE, NOTICE_FILE, NOTICE_CHECKED_FILE, LAST_PUBLISHED_FILE, ALERT_FILE, VIOLATION_FILE, RUN_REPORT_DIR'
if old2 in text: text = text.replace(old2, new2, 1)
else: errors.append('step2')

# step 3: _init_run_dir 路径
old3 = 'NOTICE_CHECKED_FILE = os.path.join(RUN_REPORT_DIR, "notice_checked.txt")  # [v1102] 已检查账号持久化'
new3 = '''NOTICE_CHECKED_FILE = os.path.join(RUN_REPORT_DIR, "notice_checked.txt")  # [v1102] 已检查账号持久化
    LAST_PUBLISHED_FILE = os.path.join(RUN_REPORT_DIR, "last_published.txt")  # [v1102.2] 最近 publish 成功账号持久化'''
if old3 in text: text = text.replace(old3, new3, 1)
else: errors.append('step3')

# step 4: _do_publish OK 后写 last_published.txt(同微头条 anchor)
old4 = '''            if success:
                move_to_sent(doc)
                if doc in doc_pool:
                    doc_pool.remove(doc)
                acc_count[name] = acc_count.get(name, 0) + 1
                success_accounts.add(name)
                ok_count += 1
                total_alerts += check_reading_stats(ws_url, name)'''
new4 = '''            if success:
                move_to_sent(doc)
                if doc in doc_pool:
                    doc_pool.remove(doc)
                acc_count[name] = acc_count.get(name, 0) + 1
                success_accounts.add(name)
                ok_count += 1
                # [v1102.2] 持久化最近 publish 成功账号
                try:
                    with open(LAST_PUBLISHED_FILE, "a", encoding="utf-8") as _lpf:
                        _lpf.write(f"{name}|{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\\n")
                except Exception as _e:
                    log(f"  [v1102.2] 写 last_published.txt 失败: {_e}")
                total_alerts += check_reading_stats(ws_url, name)'''
if old4 in text: text = text.replace(old4, new4, 1)
else: errors.append('step4')

# step 5: 文章 batch.py 加载白名单 dict 段 → v1102.1 按顺序重排 + v1102.2 中断处接续
old5 = '''        _wl_map = _read_whitelist_with_quota()
        if _wl_map:
            accounts = [a for a in accounts if any(inc in a or a in inc for inc in _wl_map.keys())]
            for a in accounts:
                for inc, q in _wl_map.items():
                    if inc in a or a in inc:
                        quota_map[a] = q
                        break
            log(f"账号配置.xlsx[白名单]已加载,白名单 {len(_wl_map)} 个,过滤后剩 {len(accounts)} 个账号")
            log(f"白名单配额: {quota_map}")'''

new5 = '''        _wl_map = _read_whitelist_with_quota()
        if _wl_map:
            # [v1102.1] 按白名单 dict 顺序重排 accounts(catchup 写白名单按断点环形排)
            _orig_accounts = list(accounts)
            _seen = set()
            _new_accounts = []
            for inc in _wl_map.keys():
                for a in _orig_accounts:
                    if a not in _seen and (inc in a or a in inc):
                        _new_accounts.append(a)
                        _seen.add(a)
                        break
            accounts = _new_accounts
            # [v1102.2] 主线主控 v2:读 last_published.txt 拿最近 publish 账号 → 找 idx → 环形重排让下一位置首
            _last_published_acc = None
            if LAST_PUBLISHED_FILE and os.path.exists(LAST_PUBLISHED_FILE):
                try:
                    with open(LAST_PUBLISHED_FILE, encoding='utf-8') as _lpf:
                        _lines = [_l.strip() for _l in _lpf if _l.strip()]
                        if _lines:
                            _last_published_acc = _lines[-1].split('|')[0].strip()
                except Exception as _e:
                    log(f"  [v1102.2] last_published.txt 读取失败: {_e}")
            if _last_published_acc and accounts:
                _last_idx = -1
                for _i, _a in enumerate(accounts):
                    if _last_published_acc in _a or _a in _last_published_acc:
                        _last_idx = _i
                        break
                if _last_idx >= 0:
                    _next = (_last_idx + 1) % len(accounts)
                    accounts = accounts[_next:] + accounts[:_next]
                    log(f"  [v1102.2] 中断处自动接续:最近 publish「{_last_published_acc}」(idx={_last_idx}) → 从下一位「{accounts[0]}」起跑")
            for a in accounts:
                for inc, q in _wl_map.items():
                    if inc in a or a in inc:
                        quota_map[a] = q
                        break
            log(f"账号配置.xlsx[白名单]已加载,白名单 {len(_wl_map)} 个,过滤+重排后剩 {len(accounts)} 个账号(首位={accounts[0] if accounts else '空'})")
            log(f"白名单配额: {quota_map}")'''

if old5 in text: text = text.replace(old5, new5, 1)
else: errors.append('step5')

if errors:
    print(f'  [{fp}] FAILED:', errors); sys.exit(1)

with open(fp, 'w', encoding='utf-8', newline='\n') as f:
    f.write(text)
print(f'  [{fp}] PATCHED')
