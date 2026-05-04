# -*- coding: utf-8 -*-
"""
v1102 patch 脚本 — 应用 5 处替换到任意 gtg_batch.py
用法: python .tmp_v1102_patch.py <gtg_batch.py 路径>
"""
import sys, re

if len(sys.argv) < 2:
    print("用法: python .tmp_v1102_patch.py <file>")
    sys.exit(1)

fp = sys.argv[1]
with open(fp, encoding='utf-8') as f:
    text = f.read()

# 防重复 patch
if 'NOTICE_CHECKED_FILE' in text:
    print(f'  [{fp}] 已含 NOTICE_CHECKED_FILE,跳过')
    sys.exit(0)

before = len(text)

# 1. NOTICE_FILE 全局变量 — 加 NOTICE_CHECKED_FILE
# Mac 版 (6 空格) 和 Win 版 (4 空格) 都处理
patterns_global = [
    ('NOTICE_FILE      = None\nALERT_FILE       = None',
     'NOTICE_FILE      = None\nNOTICE_CHECKED_FILE = None  # [v1102] 持久化已检查账号集合(中断恢复后仍只读 1 次)\nALERT_FILE       = None'),
    ('NOTICE_FILE    = None\nALERT_FILE     = None',
     'NOTICE_FILE    = None\nNOTICE_CHECKED_FILE = None  # [v1102] 持久化已检查账号集合(中断恢复后仍只读 1 次)\nALERT_FILE     = None'),
]
for old, new in patterns_global:
    if old in text:
        text = text.replace(old, new, 1)
        break
else:
    print('  ⚠ 没找到 NOTICE_FILE 全局变量段')

# 2. _init_run_dir — 加 NOTICE_CHECKED_FILE 路径 (Mac 6 空格 / Win 4 空格)
patterns_init = [
    ('global LOG_FILE, FAIL_FILE, NOTICE_FILE, ALERT_FILE, VIOLATION_FILE, RUN_REPORT_DIR',
     'global LOG_FILE, FAIL_FILE, NOTICE_FILE, NOTICE_CHECKED_FILE, ALERT_FILE, VIOLATION_FILE, RUN_REPORT_DIR'),
]
for old, new in patterns_init:
    if old in text:
        text = text.replace(old, new, 1)
        break

patterns_init2 = [
    ('NOTICE_FILE    = os.path.join(RUN_REPORT_DIR, "系统通知.txt")\n    ALERT_FILE     = os.path.join(RUN_REPORT_DIR, "高阅读提醒.txt")',
     'NOTICE_FILE    = os.path.join(RUN_REPORT_DIR, "系统通知.txt")\n    NOTICE_CHECKED_FILE = os.path.join(RUN_REPORT_DIR, "notice_checked.txt")  # [v1102] 已检查账号持久化\n    ALERT_FILE     = os.path.join(RUN_REPORT_DIR, "高阅读提醒.txt")'),
]
for old, new in patterns_init2:
    if old in text:
        text = text.replace(old, new, 1)
        break

# 3. check_system_notice 函数体 — 整段重写(用正则匹配)
# 旧版函数从 def check_system_notice 到 return 0, 0(except 末尾)
old_fn_start = text.find('def check_system_notice(ws_url, account_name):')
if old_fn_start == -1:
    print('  ⚠ 没找到 def check_system_notice')
else:
    # 找函数末尾(return 0, 0 后的空行)
    fn_end_marker = '        return 0, 0\n'
    end_idx = text.find(fn_end_marker, old_fn_start)
    if end_idx == -1:
        print('  ⚠ 没找到函数末尾 return 0, 0')
    else:
        end_idx += len(fn_end_marker)
        new_fn = '''def check_system_notice(ws_url, account_name):
    """
    [v1102] 导航到消息中心 → 点击 系统通知 + 审核通知 频道
    → 读取 2 天内(今天+昨天)的完整消息原文写入 NOTICE_FILE
    新 selector: .conversation-box.notify-im-user-item (替代旧 span.name)
    新提取: body.innerText 按日期行切分(MM-DD HH:MM / YYYY-MM-DD / 昨日/今日 HH:MM)
    """
    try:
        today = datetime.now()
        yesterday = today - timedelta(days=1)
        today_short     = today.strftime("%m-%d")
        yesterday_short = yesterday.strftime("%m-%d")
        today_full      = today.strftime("%Y-%m-%d")
        yesterday_full  = yesterday.strftime("%Y-%m-%d")

        wsc = ws_connect(ws_url, timeout=8)
        js(wsc, "location.href='https://mp.toutiao.com/profile_v4/personal/message?type=message_letter'", 300)
        wsc.close()
        time.sleep(3)

        wsc = ws_connect(ws_url, timeout=8)
        time.sleep(2.5)
        notices = []

        for channel in ["系统通知", "审核通知"]:
            channel_json = channel.replace('"', '\\\\"')
            clicked = js(wsc, f"""
            (function(){{
                var items = document.querySelectorAll('.conversation-box.notify-im-user-item');
                for(var i=0; i<items.length; i++){{
                    var t = (items[i].innerText || '').trim();
                    if(t.indexOf("{channel_json}") === 0){{
                        items[i].click();
                        return 'ok';
                    }}
                }}
                return null;
            }})()
            """, 301)

            if not clicked:
                log(f"  未找到频道: {channel}")
                continue

            time.sleep(2.5)

            result = js(wsc, f"""
            (function() {{
                var todayShort = "{today_short}";
                var yesterdayShort = "{yesterday_short}";
                var todayFull = "{today_full}";
                var yesterdayFull = "{yesterday_full}";
                var lines = (document.body.innerText || '').split(/\\\\r?\\\\n/);
                var results = [];
                var current = '';
                var currentDate = '';
                var inWindow = false;
                function dateInfo(line) {{
                    var m = line.match(/^(\\\\d{{2}}-\\\\d{{2}})\\\\s+\\\\d{{2}}:\\\\d{{2}}$/);
                    if (m) return m[1] === todayShort || m[1] === yesterdayShort;
                    m = line.match(/^(\\\\d{{4}}-\\\\d{{2}}-\\\\d{{2}})\\\\s+\\\\d{{2}}:\\\\d{{2}}$/);
                    if (m) return m[1] === todayFull || m[1] === yesterdayFull;
                    if (/^昨日\\\\s+\\\\d{{2}}:\\\\d{{2}}$/.test(line)) return true;
                    if (/^今日\\\\s+\\\\d{{2}}:\\\\d{{2}}$/.test(line)) return true;
                    return null;
                }}
                function isDateLine(line) {{
                    return /^(\\\\d{{2}}-\\\\d{{2}}|\\\\d{{4}}-\\\\d{{2}}-\\\\d{{2}}|昨日|今日)\\\\s+\\\\d{{2}}:\\\\d{{2}}$/.test(line);
                }}
                for (var i = 0; i < lines.length; i++) {{
                    var line = lines[i].trim();
                    if (!line) continue;
                    if (isDateLine(line)) {{
                        if (inWindow && current.trim()) {{
                            results.push(currentDate + '\\\\n' + current.trim());
                        }}
                        currentDate = line;
                        current = '';
                        inWindow = (dateInfo(line) === true);
                    }} else if (inWindow) {{
                        current += line + '\\\\n';
                    }}
                }}
                if (inWindow && current.trim()) {{
                    results.push(currentDate + '\\\\n' + current.trim());
                }}
                var seen = {{}};
                var dedup = [];
                for (var k = 0; k < results.length; k++) {{
                    var key = results[k].substring(0, 80);
                    if (!seen[key]) {{ seen[key] = true; dedup.push(results[k]); }}
                }}
                return JSON.stringify(dedup);
            }})()
            """, 302)

            if result:
                try:
                    msgs = json.loads(result)
                    for msg in msgs:
                        notices.append(f"【{channel}】\\n{msg}")
                except:
                    pass

        wsc.close()

        violation_count = 0
        if notices:
            ts_str = datetime.now().strftime("%Y-%m-%d %H:%M")
            violations = []
            for n in notices:
                for cat, kws in VIOLATION_KEYWORDS.items():
                    for kw in kws:
                        if kw in n:
                            violations.append((cat, n))
                            break
            content_str = f"\\n[{ts_str}] 账号 {account_name} 2 天内通知 ({len(notices)} 条):\\n"
            for n in notices:
                content_str += f"\\n--- 通知 ---\\n{n}\\n"
            content_str += "\\n" + "=" * 60 + "\\n"
            with open(NOTICE_FILE, "a", encoding="utf-8") as f:
                f.write(content_str)
            log(f"  ⚠ 2 天内通知 {len(notices)} 条 → 系统通知.txt")
            if violations:
                vcontent = f"[{ts_str}] 账号 {account_name} 违规/扣分提醒:\\n"
                for cat, msg in violations:
                    vcontent += f"  [{cat}] {msg[:300]}...\\n"
                vcontent += "\\n"
                with open(VIOLATION_FILE, "a", encoding="utf-8") as f:
                    f.write(vcontent)
                violation_count = len(violations)
                log(f"  ⚠ 违规/扣分 {violation_count} 条 → 违规提醒.txt")
        else:
            log("  系统/审核通知: 2 天内无新通知")
        return len(notices), violation_count
    except Exception as e:
        log(f"  系统通知检测出错: {e}")
        return 0, 0
'''
        text = text[:old_fn_start] + new_fn + text[end_idx:]

# 4. notice_checked_set 初始化 — 持久化加载
patterns_init_set = [
    ('    notice_checked_set = set()  # [v1101.6] 每账号每天只读 1 次审核/系统通知',
     '''    # [v1102] 每账号每天只读 1 次,持久化到 NOTICE_CHECKED_FILE,中断恢复后不重读
    notice_checked_set = set()
    if NOTICE_CHECKED_FILE and os.path.exists(NOTICE_CHECKED_FILE):
        try:
            with open(NOTICE_CHECKED_FILE, encoding='utf-8') as _ncf:
                for _line in _ncf:
                    _name = _line.strip().split('|')[0]
                    if _name:
                        notice_checked_set.add(_name)
            if notice_checked_set:
                log(f"  [v1102] 从 notice_checked.txt 恢复 {len(notice_checked_set)} 个已检查账号(中断恢复)")
        except Exception as _e:
            log(f"  [v1102] notice_checked.txt 读取失败: {_e}")'''),
]
for old, new in patterns_init_set:
    if old in text:
        text = text.replace(old, new, 1)

# 5. add(name) 同步写文件
patterns_add = [
    ('''        # [v1101.6] 每账号每天只读 1 次审核/系统通知 — 后续发文跳过
        if name not in notice_checked_set:
            nc, vc = check_system_notice(ws_url, name)
            total_notices += nc
            total_violations += vc
            notice_checked_set.add(name)
            time.sleep(2)
        else:
            log(f"  系统/审核通知:{name} 本轮已读过,跳过")''',
     '''        # [v1102] 每账号每天只读 1 次审核/系统通知 — 持久化,中断恢复后仍跳过
        if name not in notice_checked_set:
            nc, vc = check_system_notice(ws_url, name)
            total_notices += nc
            total_violations += vc
            notice_checked_set.add(name)
            try:
                with open(NOTICE_CHECKED_FILE, "a", encoding="utf-8") as _ncf:
                    _ncf.write(f"{name}|{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\\n")
            except Exception as _e:
                log(f"  [v1102] 写 notice_checked.txt 失败: {_e}")
            time.sleep(2)
        else:
            log(f"  系统/审核通知:{name} 当天已读过,跳过")'''),
]
for old, new in patterns_add:
    if old in text:
        text = text.replace(old, new, 1)

# 写回
with open(fp, 'w', encoding='utf-8', newline='\n') as f:
    f.write(text)

after = len(text)
v1102_count = text.count('v1102')
print(f'  ✅ {fp}: {before} → {after} 字符,v1102 标记 {v1102_count} 处')
