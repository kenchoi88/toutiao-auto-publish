# -*- coding: utf-8 -*-
"""v1102 v2 patch — Mac 微头条 (升级 v1 _last_idx → v2 last_published.txt)"""
import sys
fp = sys.argv[1]
with open(fp, encoding='utf-8') as f:
    text = f.read()

if 'LAST_PUBLISHED_FILE' in text and '_last_published_acc' in text:
    print(f'  [{fp}] 已 v2 patched, 跳过')
    sys.exit(0)

errors = []

# 1. 全局变量加 LAST_PUBLISHED_FILE = None
old1 = 'NOTICE_CHECKED_FILE = None  # [v1102] 持久化已检查账号集合(中断恢复后仍只读 1 次)'
new1 = 'NOTICE_CHECKED_FILE = None  # [v1102] 持久化已检查账号集合(中断恢复后仍只读 1 次)\nLAST_PUBLISHED_FILE = None  # [v1102] 持久化最近 publish 成功账号(中断恢复后从此账号下一位起跑)'
if old1 not in text:
    errors.append('step1 anchor 没找到')
else:
    text = text.replace(old1, new1, 1)

# 2. _init_run_dir global 加 LAST_PUBLISHED_FILE
old2 = 'global LOG_FILE, FAIL_FILE, NOTICE_FILE, NOTICE_CHECKED_FILE, ALERT_FILE, VIOLATION_FILE, RUN_REPORT_DIR'
new2 = 'global LOG_FILE, FAIL_FILE, NOTICE_FILE, NOTICE_CHECKED_FILE, LAST_PUBLISHED_FILE, ALERT_FILE, VIOLATION_FILE, RUN_REPORT_DIR'
if old2 not in text:
    errors.append('step2 anchor 没找到')
else:
    text = text.replace(old2, new2, 1)

# 3. _init_run_dir 路径
old3 = 'NOTICE_CHECKED_FILE = os.path.join(RUN_REPORT_DIR, "notice_checked.txt")  # [v1102] 已检查账号持久化'
new3 = 'NOTICE_CHECKED_FILE = os.path.join(RUN_REPORT_DIR, "notice_checked.txt")  # [v1102] 已检查账号持久化\n    LAST_PUBLISHED_FILE = os.path.join(RUN_REPORT_DIR, "last_published.txt")  # [v1102] 最近 publish 成功账号持久化'
if old3 not in text:
    errors.append('step3 anchor 没找到')
else:
    text = text.replace(old3, new3, 1)

# 4. _do_publish OK 后写 last_published.txt
old4 = '''                acc_count[name] = acc_count.get(name, 0) + 1
                success_accounts.add(name)
                ok_count += 1
                total_alerts += check_reading_stats(ws_url, name)'''
new4 = '''                acc_count[name] = acc_count.get(name, 0) + 1
                success_accounts.add(name)
                ok_count += 1
                # [v1102] 持久化最近 publish 成功账号 → 中断恢复时按此从下一位起跑
                try:
                    with open(LAST_PUBLISHED_FILE, "a", encoding="utf-8") as _lpf:
                        _lpf.write(f"{name}|{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\\n")
                except Exception as _e:
                    log(f"  [v1102] 写 last_published.txt 失败: {_e}")
                total_alerts += check_reading_stats(ws_url, name)'''
if old4 not in text:
    errors.append('step4 anchor 没找到')
else:
    text = text.replace(old4, new4, 1)

# 5. v1 _last_idx 段替换为 v2 last_published 段
old5 = '''            accounts = _new_accounts
            # [v1102 主线主控] 自动接续中断处:找 accounts 最末一个已发账号,环形重排让它的下一位置首
            # 版本说明 line 632「中断在第 X 轮第 Y 账号 → 重启从该轮该账号继续」
            # 不依赖用户手动跑 catchup.py
            if sent_count_map and accounts:
                _last_idx = -1
                for _i, _a in enumerate(accounts):
                    if any((_sn in _a or _a in _sn) for _sn in sent_count_map.keys()):
                        _last_idx = _i
                if _last_idx >= 0 and _last_idx + 1 < len(accounts):
                    accounts = accounts[_last_idx + 1:] + accounts[:_last_idx + 1]
                    log(f"  [v1102] 中断处自动接续:从最近成功的下一位「{accounts[0]}」起跑(中段漏发挪到末尾排队补)")
            log(f"账号配置.xlsx[白名单]已加载，白名单 {len(_wl_map)} 个，过滤+重排后剩 {len(accounts)} 个账号(首位={accounts[0] if accounts else '空'})")'''

new5 = '''            accounts = _new_accounts
            # [v1102 主线主控 v2] 自动接续中断处:读 last_published.txt 拿最近 publish 账号 → 找 idx → 环形重排让下一位置首
            # 版本说明 line 632「中断在第 X 轮第 Y 账号 → 重启从该轮该账号继续」
            _last_published_acc = None
            if LAST_PUBLISHED_FILE and os.path.exists(LAST_PUBLISHED_FILE):
                try:
                    with open(LAST_PUBLISHED_FILE, encoding='utf-8') as _lpf:
                        _lines = [_l.strip() for _l in _lpf if _l.strip()]
                        if _lines:
                            _last_published_acc = _lines[-1].split('|')[0].strip()
                except Exception as _e:
                    log(f"  [v1102] last_published.txt 读取失败: {_e}")
            if _last_published_acc and accounts:
                _last_idx = -1
                for _i, _a in enumerate(accounts):
                    if _last_published_acc in _a or _a in _last_published_acc:
                        _last_idx = _i
                        break
                if _last_idx >= 0:
                    _next = (_last_idx + 1) % len(accounts)
                    accounts = accounts[_next:] + accounts[:_next]
                    log(f"  [v1102] 中断处自动接续:最近 publish「{_last_published_acc}」(idx={_last_idx}) → 从下一位「{accounts[0]}」起跑")
            log(f"账号配置.xlsx[白名单]已加载，白名单 {len(_wl_map)} 个，过滤+重排后剩 {len(accounts)} 个账号(首位={accounts[0] if accounts else '空'})")'''

if old5 not in text:
    errors.append('step5 anchor 没找到 (v1 段)')
else:
    text = text.replace(old5, new5, 1)

if errors:
    print(f'  [{fp}] FAILED:', errors)
    sys.exit(1)

with open(fp, 'w', encoding='utf-8', newline='\n') as f:
    f.write(text)
print(f'  [{fp}] PATCHED')
