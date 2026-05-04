# -*- coding: utf-8 -*-
"""v1102.2 主线主控 v2 — Mac timer.py 专用(只加 v1102.2,timer 已天然按白名单顺序不需 v1102.1 重排)"""
import sys, os
if len(sys.argv) < 2:
    print("用法: python script.py <gtg_timer.py>"); sys.exit(1)
fp = sys.argv[1]
with open(fp, encoding='utf-8') as f:
    text = f.read()

if 'LAST_PUBLISHED_FILE' in text and '_last_published_acc' in text:
    print(f'  [{fp}] 已 patched, 跳过'); sys.exit(0)

errors = []

# step 1: 全局 LAST_PUBLISHED_FILE = None
old1 = 'NOTICE_CHECKED_FILE = None  # notice_checked.txt 持久化已检查账号'
new1 = '''NOTICE_CHECKED_FILE = None  # notice_checked.txt 持久化已检查账号
LAST_PUBLISHED_FILE = None  # [v1102] 持久化最近 publish 成功账号'''
if old1 in text: text = text.replace(old1, new1, 1)
else: errors.append('step1')

# step 2: _init_run_dir global 加
old2 = 'global LOG_FILE, FAIL_FILE, RUN_REPORT_DIR, NOTICE_FILE, NOTICE_CHECKED_FILE, VIOLATION_FILE'
new2 = 'global LOG_FILE, FAIL_FILE, RUN_REPORT_DIR, NOTICE_FILE, NOTICE_CHECKED_FILE, LAST_PUBLISHED_FILE, VIOLATION_FILE'
if old2 in text: text = text.replace(old2, new2, 1)
else: errors.append('step2')

# step 3: _init_run_dir 路径加
old3 = 'NOTICE_CHECKED_FILE = os.path.join(RUN_REPORT_DIR, "notice_checked.txt")'
new3 = '''NOTICE_CHECKED_FILE = os.path.join(RUN_REPORT_DIR, "notice_checked.txt")
    LAST_PUBLISHED_FILE = os.path.join(RUN_REPORT_DIR, "last_published.txt")'''
if old3 in text: text = text.replace(old3, new3, 1)
else: errors.append('step3')

# step 4: publish_article_timer success 后写 last_published.txt
old4 = '''    log(f"  OK 定时发布成功 → {timer_time}")
    return True, "成功"'''
new4 = '''    log(f"  OK 定时发布成功 → {timer_time}")
    # [v1102] 持久化最近 publish 成功账号
    try:
        with open(LAST_PUBLISHED_FILE, "a", encoding="utf-8") as _lpf:
            _lpf.write(f"{account_name}|{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\\n")
    except Exception as _e:
        log(f"  [v1102] 写 last_published.txt 失败: {_e}")
    return True, "成功"'''
if old4 in text: text = text.replace(old4, new4, 1)
else: errors.append('step4')

# step 5: main 在 all_accounts 构造完后,加读 last_published.txt + 环形重排
old5 = '''    if not all_accounts:
        log("错误: 没有可发文账号")
        main_ws.close()
        return'''
new5 = '''    if not all_accounts:
        log("错误: 没有可发文账号")
        main_ws.close()
        return

    # [v1102] 主线主控 v2:读 last_published.txt 拿最近 publish 账号 → 找 idx → 环形重排让下一位置首
    _last_published_acc = None
    if LAST_PUBLISHED_FILE and os.path.exists(LAST_PUBLISHED_FILE):
        try:
            with open(LAST_PUBLISHED_FILE, encoding='utf-8') as _lpf:
                _lines = [_l.strip() for _l in _lpf if _l.strip()]
                if _lines:
                    _last_published_acc = _lines[-1].split('|')[0].strip()
        except Exception as _e:
            log(f"  [v1102] last_published.txt 读取失败: {_e}")
    if _last_published_acc and all_accounts:
        _last_idx = -1
        for _i, _a in enumerate(all_accounts):
            if _last_published_acc in _a or _a in _last_published_acc:
                _last_idx = _i
                break
        if _last_idx >= 0:
            _next = (_last_idx + 1) % len(all_accounts)
            all_accounts = all_accounts[_next:] + all_accounts[:_next]
            log(f"  [v1102] 中断处自动接续:最近 publish「{_last_published_acc}」(idx={_last_idx}) → 从下一位「{all_accounts[0]}」起跑")'''

if old5 in text: text = text.replace(old5, new5, 1)
else: errors.append('step5')

if errors:
    print(f'  [{fp}] FAILED:', errors); sys.exit(1)

with open(fp, 'w', encoding='utf-8', newline='\n') as f:
    f.write(text)
print(f'  [{fp}] PATCHED')
