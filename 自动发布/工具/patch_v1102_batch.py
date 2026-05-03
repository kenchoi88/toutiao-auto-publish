"""
v1102 batch 件 (微头条 / 文章) 主线内化中断恢复 patch
"""
import sys, os, time

def patch(path):
    if not os.path.exists(path):
        print(f"[FAIL] 不存在: {path}"); return False
    src = open(path, encoding='utf-8').read()
    orig = src
    bak = f"{path}.bak_pre_v1102_{time.strftime('%Y%m%d_%H%M%S')}"
    open(bak, 'w', encoding='utf-8').write(src)
    print(f"[BAK] {bak}")

    if 'v1102' in src and 'initial_acc_count=sent_count_map' in src:
        print(f"[SKIP] 已 patch v1102")
        return True

    fails = []

    # 1. _append_sent_excel 升级为 (账号, count) 累加 — regex 兼容 Win/Mac docstring 差异
    import re
    a1_pattern = re.compile(
        r'def _append_sent_excel\(name\):\n'
        r'(?:    """[^"]*"""\n)?'
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
        r'        pass'
    )
    a1_old = a1_pattern.search(src)
    a1_new = '''def _append_sent_excel(name):
    """[v1102] 写「本轮已发」sheet:行存在 count+1,不存在 append (账号, 1)"""
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
    """[v1102] 读「本轮已发」sheet → {账号: 已发次数}"""
    if not os.path.exists(CONFIG_EXCEL):
        return {}
    try:
        wb = openpyxl.load_workbook(CONFIG_EXCEL, read_only=True, data_only=True)
        if "本轮已发" not in wb.sheetnames:
            wb.close(); return {}
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
        wb.close()
        return result
    except Exception:
        return {}'''
    if a1_old:
        src = src.replace(a1_old.group(0), a1_new); print('[OK] anchor1 _append_sent_excel + _read_sent_with_count')
    else: fails.append('1.append_sent')

    # 2. 小轮末 _clear_round_sheets() 调用 → 移到大循环末(全员齐活才 clear)
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
        src = src.replace(a2_old, a2_new); print('[OK] anchor2 clear 时机移到大循环末')
    else: fails.append('2.clear timing')

    # 3. main() default_q 改加 sent_total — 用 regex 兼容微头条/文章 batch 不同注释
    import re
    a3_pattern = re.compile(r'(    per_account_quota = \{\}\n\n)((?:    # [^\n]*\n)?)(    whitelist_with_q = _read_whitelist_with_quota\(\))')
    if a3_pattern.search(src):
        src = a3_pattern.sub(r'\1    # [v1102] quota 动态算 = (素材池 + 已发累计) // 账号数\n    sent_count_map = _read_sent_with_count()\n    sent_total = sum(sent_count_map.values())\n\n\2\3', src, count=1)
        print('[OK] anchor3 main 起步 sent_count_map')
    else: fails.append('3.main sent_map')

    # 4. default_q = max(1, len(docs) // len(accounts)) → max(1, (len(docs) + sent_total) // len(accounts))
    a4_old = '        default_q = max(1, len(docs) // len(accounts)) if accounts else 1'
    a4_new = '        default_q = max(1, (len(docs) + sent_total) // len(accounts)) if accounts else 1'
    if a4_old in src:
        n_a4 = src.count(a4_old)
        src = src.replace(a4_old, a4_new); print(f'[OK] anchor4 default_q 加 sent_total ({n_a4} 处)')
    else: fails.append('4.default_q')

    # 5. run_death_grip 调用加 initial_acc_count
    a5_old = '''        sent_accounts_set=sent_accounts_set,
        credit_records=credit_records,
    )'''
    a5_new = '''        sent_accounts_set=sent_accounts_set,
        credit_records=credit_records,
        initial_acc_count=sent_count_map,  # [v1102] 传入已发次数
    )'''
    if a5_old in src:
        src = src.replace(a5_old, a5_new); print('[OK] anchor5 run_death_grip 传 initial_acc_count')
    else: fails.append('5.initial_acc_count')

    if fails:
        print(f"[FAIL] 锚点未命中: {fails}")
        open(path, 'w', encoding='utf-8').write(orig)
        os.remove(bak)
        print("[ROLLBACK]"); return False

    open(path, 'w', encoding='utf-8').write(src)
    try:
        import py_compile
        py_compile.compile(path, doraise=True)
        print("[OK] py_compile")
    except Exception as e:
        print(f"[FAIL] py_compile: {e}")
        open(path, 'w', encoding='utf-8').write(orig)
        os.remove(bak)
        return False
    return True

if __name__ == "__main__":
    if len(sys.argv) < 2: print("用法: python patch_v1102_batch.py <gtg_batch.py>"); sys.exit(1)
    sys.exit(0 if patch(sys.argv[1]) else 1)
