# -*- coding: utf-8 -*-
"""v1102 NOTICE 重建 — Mac timer.py(漏 patch 补)
   用法: python .tmp_v1102_notice_timer_mac.py <gtg_timer.py 路径> [batch.py 路径]
   不传第二个参数 = 从 ~/Desktop/微头条自动发布/gtg_batch.py 读 check_system_notice
"""
import sys, re, os

if len(sys.argv) < 2:
    print("用法: python script.py <gtg_timer.py> [batch.py]"); sys.exit(1)

fp = sys.argv[1]
batch_fp = sys.argv[2] if len(sys.argv) > 2 else os.path.expanduser('~/Desktop/微头条自动发布/gtg_batch.py')

with open(fp, encoding='utf-8') as f:
    text = f.read()

if 'check_system_notice' in text and 'NOTICE_CHECKED_FILE' in text:
    print(f'  [{fp}] 已 patched, 跳过'); sys.exit(0)

# 从 batch.py 读 check_system_notice 函数体(到 return 0, 0 后第一个空行)
with open(batch_fp, encoding='utf-8') as f:
    batch_text = f.read()
m = re.search(r'(def check_system_notice\(ws_url, account_name\):.*?\n        return 0, 0\n)', batch_text, re.DOTALL)
if not m:
    print(f'  ❌ batch.py 没找到 check_system_notice'); sys.exit(1)
check_func_code = m.group(1)

# _check_notice_once wrapper(timer.py 用)
wrapper_code = '''
def _check_notice_once(ws_url, account_name):
    """[v1102] publish 调用前 wrapper: 当天读 1 次 NOTICE,持久化 set"""
    global notice_checked_set
    if account_name in notice_checked_set:
        log(f"  系统/审核通知:{account_name} 当天已读过,跳过")
        return
    check_system_notice(ws_url, account_name)
    notice_checked_set.add(account_name)
    try:
        with open(NOTICE_CHECKED_FILE, "a", encoding="utf-8") as _ncf:
            _ncf.write(f"{account_name}|{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\\n")
    except Exception as _e:
        log(f"  [v1102] 写 notice_checked.txt 失败: {_e}")


'''

errors = []

# step 1: 全局变量
old1 = 'ALERT_FILE = None  # 在 _init_run_dir 里赋值\nLOG_FILE       = None\nFAIL_FILE      = None'
new1 = '''ALERT_FILE = None  # 在 _init_run_dir 里赋值
LOG_FILE       = None
FAIL_FILE      = None
# [v1102 NOTICE 重建] timer.py 补
NOTICE_FILE         = None  # 系统通知.txt
NOTICE_CHECKED_FILE = None  # notice_checked.txt 持久化已检查账号
VIOLATION_FILE      = None  # 违规提醒.txt
notice_checked_set  = set()  # 全局: 当天已检查 NOTICE 账号'''
if old1 in text: text = text.replace(old1, new1, 1)
else: errors.append('step1')

# step 2: _init_run_dir global
old2 = '    global LOG_FILE, FAIL_FILE, RUN_REPORT_DIR'
new2 = '    global LOG_FILE, FAIL_FILE, RUN_REPORT_DIR, NOTICE_FILE, NOTICE_CHECKED_FILE, VIOLATION_FILE'
if old2 in text: text = text.replace(old2, new2, 1)
else: errors.append('step2')

# step 3: _init_run_dir 路径
old3 = '    global ALERT_FILE\n    ALERT_FILE = os.path.join(RUN_REPORT_DIR, "高阅读量提醒.txt")'
new3 = '''    global ALERT_FILE
    ALERT_FILE = os.path.join(RUN_REPORT_DIR, "高阅读量提醒.txt")
    NOTICE_FILE         = os.path.join(RUN_REPORT_DIR, "系统通知.txt")
    NOTICE_CHECKED_FILE = os.path.join(RUN_REPORT_DIR, "notice_checked.txt")
    VIOLATION_FILE      = os.path.join(RUN_REPORT_DIR, "违规提醒.txt")'''
if old3 in text: text = text.replace(old3, new3, 1)
else: errors.append('step3')

# step 4: 在 def publish_article_timer 之前插入 check_system_notice 函数 + wrapper
old4 = 'def publish_article_timer(ws_url, doc_path, main_ws, account_name, timer_time=None):'
new4 = check_func_code + wrapper_code + 'def publish_article_timer(ws_url, doc_path, main_ws, account_name, timer_time=None):'
if old4 in text: text = text.replace(old4, new4, 1)
else: errors.append('step4')

# step 5: main 加 notice_checked_set 从文件恢复
old5 = '''def main():
    _init_run_dir()
    log("=" * 50)'''
new5 = '''def main():
    _init_run_dir()
    # [v1102] 从 notice_checked.txt 恢复 notice_checked_set
    global notice_checked_set
    notice_checked_set = set()
    if NOTICE_CHECKED_FILE and os.path.exists(NOTICE_CHECKED_FILE):
        try:
            with open(NOTICE_CHECKED_FILE, encoding='utf-8') as _ncf:
                for _line in _ncf:
                    _name = _line.strip().split('|')[0]
                    if _name:
                        notice_checked_set.add(_name)
        except Exception as _e:
            pass
    log("=" * 50)'''
if old5 in text: text = text.replace(old5, new5, 1)
else: errors.append('step5')

# step 5b: 启动 log 显示恢复条数
old5b = 'log(f"报告目录: {RUN_REPORT_DIR}")\n    log("=" * 50)'
new5b = '''log(f"报告目录: {RUN_REPORT_DIR}")
    if notice_checked_set:
        log(f"  [v1102] 从 notice_checked.txt 恢复 {len(notice_checked_set)} 个已检查账号(中断恢复)")
    log("=" * 50)'''
if old5b in text: text = text.replace(old5b, new5b, 1)

# step 6: publish_article_timer 函数体顶部加 NOTICE 检查
old6 = '''def publish_article_timer(ws_url, doc_path, main_ws, account_name, timer_time=None):
    """定时发布一篇文章，timer_time格式: YYYY-MM-DD HH:MM"""
    try:
        wsc = ws_connect(ws_url, timeout=10)'''
new6 = '''def publish_article_timer(ws_url, doc_path, main_ws, account_name, timer_time=None):
    """定时发布一篇文章，timer_time格式: YYYY-MM-DD HH:MM"""
    # [v1102] publish 前检 NOTICE(每号当天 1 次,持久化)
    _check_notice_once(ws_url, account_name)
    try:
        wsc = ws_connect(ws_url, timeout=10)'''
if old6 in text: text = text.replace(old6, new6, 1)
else: errors.append('step6')

if errors:
    print(f'  [{fp}] FAILED:', errors); sys.exit(1)

with open(fp, 'w', encoding='utf-8', newline='\n') as f:
    f.write(text)
print(f'  [{fp}] PATCHED')
