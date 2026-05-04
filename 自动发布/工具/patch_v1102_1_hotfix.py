# -*- coding: utf-8 -*-
"""v1102.1 hotfix — 白名单顺序重排 (catchup 接续 bug 修复)"""
import sys
fp = sys.argv[1]
with open(fp, encoding='utf-8') as f:
    text = f.read()

if 'v1102.1' in text or '过滤+重排后' in text:
    print(f'  [{fp}] 已含 v1102.1,跳过')
    sys.exit(0)

# 两种变量名(Win 台机 = whitelist_with_q,Mac = _wl_q)
patterns = [
    # Win 台机版
    ('''    whitelist_with_q = _read_whitelist_with_quota()
    if whitelist_with_q:
        wl_map = {n: q for n, q in whitelist_with_q}
        accounts = [a for a in accounts if any(wn in a or a in wn for wn in wl_map)]
        log(f"账号配置.xlsx[白名单]已加载，白名单 {len(wl_map)} 个，过滤后剩 {len(accounts)} 个账号")''',
     '''    whitelist_with_q = _read_whitelist_with_quota()
    if whitelist_with_q:
        wl_map = {n: q for n, q in whitelist_with_q}
        # [v1102.1] 按白名单顺序重排 accounts(catchup 写白名单是环形重排,主循环必须用此顺序才能从断点开始)
        _orig_accounts = list(accounts)
        _new_accounts = []
        _seen = set()
        for wn, _wq in whitelist_with_q:
            for a in _orig_accounts:
                if a not in _seen and (wn in a or a in wn):
                    _new_accounts.append(a)
                    _seen.add(a)
                    break
        accounts = _new_accounts
        log(f"账号配置.xlsx[白名单]已加载，白名单 {len(wl_map)} 个，过滤+重排后剩 {len(accounts)} 个账号(首位={accounts[0] if accounts else '空'})")'''),
    # Mac 版(_wl_q,带 quota_map 处理)
    ('''        _wl_q = _read_whitelist_with_quota()
        if _wl_q:
            _wl_map = {n: q for n, q in _wl_q}
            accounts = [a for a in accounts if any(wn in a or a in wn for wn in _wl_map)]
            log(f"账号配置.xlsx[白名单]已加载，白名单 {len(_wl_map)} 个，过滤后剩 {len(accounts)} 个账号")''',
     '''        _wl_q = _read_whitelist_with_quota()
        if _wl_q:
            _wl_map = {n: q for n, q in _wl_q}
            # [v1102.1] 按白名单顺序重排 accounts(catchup 写白名单是环形重排,主循环必须用此顺序才能从断点开始)
            _orig_accounts = list(accounts)
            _new_accounts = []
            _seen = set()
            for wn, _wq in _wl_q:
                for a in _orig_accounts:
                    if a not in _seen and (wn in a or a in wn):
                        _new_accounts.append(a)
                        _seen.add(a)
                        break
            accounts = _new_accounts
            log(f"账号配置.xlsx[白名单]已加载，白名单 {len(_wl_map)} 个，过滤+重排后剩 {len(accounts)} 个账号(首位={accounts[0] if accounts else '空'})")'''),
]

matched = False
for old, new in patterns:
    if old in text:
        text = text.replace(old, new, 1)
        matched = True
        break

if not matched:
    print(f'  [{fp}] 没找到任何匹配段,跳过')
    sys.exit(0)
with open(fp, 'w', encoding='utf-8', newline='\n') as f:
    f.write(text)
print(f'  [{fp}] v1102.1 patch OK')
