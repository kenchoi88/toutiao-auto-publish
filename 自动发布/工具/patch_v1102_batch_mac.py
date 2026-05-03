"""v1102 Mac batch (微头条 / 文章) patch"""
import sys, os, time, re

def patch(path):
    if not os.path.exists(path): print(f"[FAIL] 不存在: {path}"); return False
    src = open(path, encoding='utf-8').read(); orig = src
    bak = f"{path}.bak_pre_v1102_{time.strftime('%Y%m%d_%H%M%S')}"
    open(bak, 'w', encoding='utf-8').write(src); print(f"[BAK] {bak}")

    if 'v1102' in src and 'initial_acc_count=sent_count_map' in src:
        print("[SKIP]"); return True

    fails = []

    # 1. _append_sent_excel(Mac 带 docstring)+ 加 _read_sent_with_count
    a1 = re.search(
        r'def _append_sent_excel\(name\):\n'
        r'    """[^"]*"""\n'
        r'    try:\n'
        r'        _ensure_config_excel\(\)\n'
        r'        wb = openpyxl\.load_workbook\(CONFIG_EXCEL\)\n'
        r'        if "本轮已发" not in wb\.sheetnames:\n'
        r'            ws_s = wb\.create_sheet\("本轮已发"\)\n'
        r'            ws_s\.append\(\["账号名"\]\)\n'
        r'        else:\n'
        r'            ws_s = wb\["本轮已发"\]\n'
        r'        ws_s\.append\(\[name\]\)\n'
        r'        wb\.save\(CONFIG_EXCEL\)\n'
        r'    except Exception:\n'
        r'        pass', src)
    a1_new = '''def _append_sent_excel(name):
    """[v1102] 写「本轮已发」 sheet:行存在 count+1,不存在 append (账号, 1)"""
    try:
        _ensure_config_excel()
        wb = openpyxl.load_workbook(CONFIG_EXCEL)
        if "本轮已发" not in wb.sheetnames:
            ws_s = wb.create_sheet("本轮已发")
            ws_s.append(["账号名", "已发次数"])
            ws_s.append([name, 1])
        else:
            ws_s = wb["本轮已发"]
            found_row = None
            for row_idx, row in enumerate(ws_s.iter_rows(min_row=2, max_col=2, values_only=False), start=2):
                if row[0].value and str(row[0].value).strip() == name:
                    found_row = row_idx
                    break
            if found_row:
                cur = ws_s.cell(row=found_row, column=2).value or 0
                try: cur = int(cur)
                except: cur = 0
                ws_s.cell(row=found_row, column=2).value = cur + 1
            else:
                ws_s.append([name, 1])
        wb.save(CONFIG_EXCEL)
    except Exception:
        pass


def _read_sent_with_count():
    """[v1102] 读「本轮已发」 sheet → {账号: 已发次数}"""
    if not os.path.exists(CONFIG_EXCEL): return {}
    try:
        wb = openpyxl.load_workbook(CONFIG_EXCEL, read_only=True, data_only=True)
        if "本轮已发" not in wb.sheetnames: wb.close(); return {}
        ws_r = wb["本轮已发"]
        result = {}
        for row in ws_r.iter_rows(min_row=2, max_col=2, values_only=True):
            if not row or not row[0]: continue
            name = str(row[0]).strip()
            if not name or name.startswith('#'): continue
            cnt = 1
            if len(row) > 1 and row[1] is not None:
                try: cnt = int(row[1])
                except: cnt = 1
            result[name] = cnt
        wb.close(); return result
    except Exception:
        return {}'''
    if a1:
        src = src.replace(a1.group(0), a1_new); print('[OK] anchor1')
    else: fails.append('1.append')

    # 2. clear 时机 — 跟 Win 同款
    a2_old = '''            sent_accounts_set.clear()
            _clear_round_sheets()

        log(f"\\n{'='*20} {log_label}第 {big_round} 大循环 结束 {'='*20}")'''
    a2_new = '''            sent_accounts_set.clear()
            # [v1102] sheet 不再小轮末 clear,累积到大循环末才 clear

        log(f"\\n{'='*20} {log_label}第 {big_round} 大循环 结束 {'='*20}")
        # [v1102] 全员齐活才 clear 「本轮已发」 sheet
        active_left = [a for a in accounts if a not in dead_terminated and acc_count.get(a, 0) < per_account_quota.get(a, 0)]
        if not active_left:
            _clear_round_sheets()
            log(f"  [v1102] 大循环全员齐活 → 「本轮已发」 sheet 已清空")'''
    if a2_old in src:
        src = src.replace(a2_old, a2_new); print('[OK] anchor2')
    else: fails.append('2.clear')

    # 3. Mac main: _read_excel_sheet("本轮已发") → _read_sent_with_count + 算 sent_total
    a3_old = '''    # 读取账号配置.xlsx - 本轮已发sheet（中断恢复时跳过已发账号）
    sent_accounts_set = set()
    try:
        _sent_list = _read_excel_sheet("本轮已发")
        for _sv in _sent_list:
            sent_accounts_set.add(_sv)
        if sent_accounts_set:
            log(f"账号配置.xlsx[本轮已发]已加载，本轮已发: {len(sent_accounts_set)} 个账号（本轮将跳过）")
    except Exception as _se:
        log(f"读取账号配置.xlsx[本轮已发]失败: {_se}")'''
    a3_new = '''    # [v1102] 读「本轮已发」sheet → {账号: 已发次数} + 注入 sent_accounts_set
    sent_accounts_set = set()
    sent_count_map = {}
    try:
        sent_count_map = _read_sent_with_count()
        for _sv in sent_count_map:
            sent_accounts_set.add(_sv)
        if sent_count_map:
            log(f"账号配置.xlsx[本轮已发]已加载,已发累计 {sum(sent_count_map.values())} 篇 / {len(sent_count_map)} 个账号")
    except Exception as _se:
        log(f"读取账号配置.xlsx[本轮已发]失败: {_se}")
    sent_total = sum(sent_count_map.values())'''
    if a3_old in src:
        src = src.replace(a3_old, a3_new); print('[OK] anchor3')
    else: fails.append('3.main sent_map')

    # 4. quota = len(docs) // len(accounts) → (len(docs) + sent_total) // len(accounts)
    a4_old = '        quota = len(docs) // len(accounts) if len(accounts) > 0 else 1'
    a4_new = '        quota = (len(docs) + sent_total) // len(accounts) if len(accounts) > 0 else 1  # [v1102] 加已发累计'
    if a4_old in src:
        src = src.replace(a4_old, a4_new); print('[OK] anchor4')
    else: fails.append('4.quota')

    # 5. run_death_grip 调用加 initial_acc_count(Mac 已有 fail_records / success_accounts 等参数,直接加在末尾)
    a5_old = '''        sent_accounts_set=sent_accounts_set,
        credit_records=credit_records,
        fail_records=fail_records,
        success_accounts=success_accounts,
    )'''
    a5_new = '''        sent_accounts_set=sent_accounts_set,
        credit_records=credit_records,
        fail_records=fail_records,
        success_accounts=success_accounts,
        initial_acc_count=sent_count_map,  # [v1102] 传入已发次数,主循环 acc_count<quota 自然停
    )'''
    if a5_old in src:
        src = src.replace(a5_old, a5_new); print('[OK] anchor5')
    else: fails.append('5.run_death_grip')

    if fails:
        print(f"[FAIL] {fails}")
        open(path, 'w', encoding='utf-8').write(orig); os.remove(bak)
        print("[ROLLBACK]"); return False

    open(path, 'w', encoding='utf-8').write(src)
    try:
        import py_compile; py_compile.compile(path, doraise=True); print("[OK] py_compile")
    except Exception as e:
        print(f"[FAIL] py_compile: {e}")
        open(path, 'w', encoding='utf-8').write(orig); os.remove(bak); return False
    return True

if __name__ == "__main__":
    if len(sys.argv) < 2: sys.exit(1)
    sys.exit(0 if patch(sys.argv[1]) else 1)
