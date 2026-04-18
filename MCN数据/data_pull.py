#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# MCN流量对比 - 每天运行一次，追加今日统计列到流量对比汇总.xlsx

import sqlite3, os, sys, json, requests, urllib.request, websocket
import zipfile, io, xml.etree.ElementTree as ET, time, re, warnings
from datetime import date, timedelta
from openpyxl import load_workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

warnings.filterwarnings('ignore')

PARTITION_DIR    = os.path.expanduser("~/Library/Application Support/创作罐头/Partitions")
MAIN_COOKIE      = os.path.expanduser("~/Library/Application Support/创作罐头/Cookies")
MOTHER_PARTITION = "7477169161966321683"
XLSX_PATH        = os.path.join(os.path.dirname(__file__), "流量对比汇总.xlsx")

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
    'Referer': 'https://mp.toutiao.com/profile_v4/lab/matrix_manage/content'
}

# ── Cookie ────────────────────────────────────────────────
def load_cookies_sqlite():
    cookies = {}
    for f in [MAIN_COOKIE, os.path.join(PARTITION_DIR, MOTHER_PARTITION, "Cookies")]:
        if not os.path.exists(f): continue
        try:
            conn = sqlite3.connect(f"file:{f}?mode=ro", uri=True)
            cur  = conn.cursor()
            cur.execute("SELECT name, value FROM cookies WHERE host_key LIKE '%toutiao%' OR host_key LIKE '%bytedance%'")
            for name, val in cur.fetchall(): cookies[name] = val
            conn.close()
        except: pass
    return cookies

def load_cookies_cdp():
    port_file = os.path.expanduser("~/Library/Application Support/创作罐头/DevToolsActivePort")
    port = int(open(port_file).readline().strip())
    try:
        pages = json.loads(urllib.request.urlopen(f'http://localhost:{port}/json', timeout=5).read())
    except Exception as e:
        print(f"  连不上罐头CDP: {e}"); return {}
    target = next((p for p in pages if 'matrix_manage' in p.get('url','') and p.get('type')=='webview'), None)
    if not target:
        target = next((p for p in pages if 'toutiao' in p.get('url','') and p.get('type')=='webview'), None)
    if not target: return {}
    try:
        ws = websocket.create_connection(target['webSocketDebuggerUrl'], timeout=10, suppress_origin=True)
        ws.send(json.dumps({'id':1,'method':'Network.getCookies','params':{'urls':['https://mp.toutiao.com']}}))
        deadline = time.time() + 8
        while time.time() < deadline:
            msg = json.loads(ws.recv())
            if msg.get('id') == 1:
                cookies = {c['name']:c['value'] for c in msg['result']['cookies']}
                ws.close(); return cookies
    except: pass
    return {}

# ── 解析头条导出xlsx ──────────────────────────────────────
def parse_export_xlsx(content):
    if not content or content[:2] != b'PK': return []
    ns = {'s': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
    zf = zipfile.ZipFile(io.BytesIO(content))
    shared = []
    if 'xl/sharedStrings.xml' in zf.namelist():
        tree = ET.parse(zf.open('xl/sharedStrings.xml'))
        for si in tree.getroot().findall('.//s:si', ns):
            shared.append(''.join(t.text or '' for t in si.findall('.//s:t', ns)))
    sheets = sorted(n for n in zf.namelist() if n.startswith('xl/worksheets/sheet'))
    if not sheets: return []
    tree = ET.parse(zf.open(sheets[0]))
    rows = []
    for row_el in tree.getroot().findall('.//s:row', ns):
        vals = []
        for c in row_el.findall('s:c', ns):
            v = c.find('s:v', ns); t = c.get('t', '')
            if v is None: vals.append('')
            elif t == 's': vals.append(shared[int(v.text)] if v.text else '')
            else: vals.append(v.text or '')
        rows.append(vals)
    zf.close()
    return rows

def fetch_day(cookies, pub_date: date, content_type: int):
    day_str = pub_date.strftime('%Y-%m-%d')
    all_rows, page = [], 1
    while True:
        url = (f"https://mp.toutiao.com/mp/agw/media_matrix/export"
               f"?from={day_str}&to={day_str}&type={content_type}&page_num={page}&size=1000")
        try:
            r = requests.get(url, cookies=cookies, headers=HEADERS, timeout=30)
            rows = parse_export_xlsx(r.content)
            data = rows[1:] if len(rows) > 1 else []
            all_rows.extend(data)
            if len(data) < 1000: break
            page += 1
        except Exception as e:
            print(f"    {day_str} 失败: {e}"); break
    recommend = read = 0
    for row in all_rows:
        if content_type == 3:  # 微头条：阅读量在 index 2，无推荐量列
            try: read += int(float(row[2])) if len(row) > 2 and row[2] else 0
            except: pass
        else:  # 文章：推荐量 index 2，阅读量 index 3
            try: recommend += int(float(row[2])) if len(row) > 2 and row[2] else 0
            except: pass
            try: read += int(float(row[3])) if len(row) > 3 and row[3] else 0
            except: pass
    return {'total': len(all_rows), 'recommend': recommend, 'read': read}

def fetch_income_day(cookies, day: date):
    day_str = day.strftime('%Y%m%d')
    all_rows, page = [], 1
    while True:
        url = (f"https://mp.toutiao.com/mp/agw/statistic/matrix/matrix_media_daily_stat_export"
               f"?start_date={day_str}&end_date={day_str}&pagenum={page}&pagesize=50")
        try:
            r = requests.get(url, cookies=cookies, headers=HEADERS, timeout=30)
            rows = parse_export_xlsx(r.content)
            data = rows[1:] if len(rows) > 1 else []
            all_rows.extend(data)
            if len(data) < 50: break
            page += 1
        except Exception as e:
            print(f"    {day_str} 收益失败: {e}"); break
    fawen = tj = yd = 0
    liuzhuan = 0.0
    for row in all_rows:
        def g(i, cast=int):
            try: return cast(float(row[i])) if len(row) > i and row[i] else 0
            except: return 0
        fawen    += g(3)
        tj       += g(4)
        yd       += g(5)
        liuzhuan += g(11, float)
    return {'fawen': fawen, 'tj': tj, 'yd': yd, 'liuzhuan': liuzhuan}

# ── 样式 ─────────────────────────────────────────────────
NEW_FILL = PatternFill("solid", fgColor="375623")
WHT_FONT = Font(color="FFFFFF", bold=True)
BLD_FONT = Font(bold=True)
CENTER   = Alignment(horizontal='center', vertical='center')
THIN     = Side(style='thin', color='CCCCCC')
BORDER   = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)

def sc(ws, row, col, val, fill=None, font=None):
    c = ws.cell(row=row, column=col, value=val)
    c.alignment = CENTER; c.border = BORDER
    if isinstance(val, (int, float)):
        c.number_format = '#,##0'
    if fill: c.fill = fill
    if font: c.font = font

def parse_date_label(label, year=2026):
    m = re.match(r'(\d+)月(\d+)号', str(label or ''))
    if m: return date(year, int(m.group(1)), int(m.group(2)))
    return None

def date_to_label(d: date):
    return f"{d.month}月{d.day}号"

# ── 主逻辑 ───────────────────────────────────────────────
def append_to_xlsx(stat_date: date, xg_cookies, jj_cookies):
    if not os.path.exists(XLSX_PATH):
        print(f"找不到 {XLSX_PATH}"); return

    wb = load_workbook(XLSX_PATH)
    stat_day = f"{stat_date.day}号"   # "19号"
    pub_date  = stat_date - timedelta(days=1)
    pub_label = date_to_label(pub_date)  # "4月18号"

    for sheet_name in wb.sheetnames:
        ws = wb[sheet_name]
        cookies  = xg_cookies if '小馆' in sheet_name else jj_cookies

        if '收益' in sheet_name:
            existing = {}
            for r in range(2, ws.max_row + 1):
                lbl = ws.cell(r, 1).value
                if lbl: existing[str(lbl)] = r
            # 只到 stat_date-1（当天数据未结算，推荐/阅读会复用前一天值）
            d = date(stat_date.year, stat_date.month, 1)
            while d < stat_date:
                lbl = date_to_label(d)
                row_idx = existing.get(lbl)
                if row_idx and ws.cell(row_idx, 5).value not in (None, '', 0, '-'):
                    d += timedelta(days=1); continue
                data = fetch_income_day(cookies, d)
                if data['fawen'] == 0 and data['liuzhuan'] == 0:
                    d += timedelta(days=1); continue
                if row_idx is None:
                    row_idx = ws.max_row + 1
                    sc(ws, row_idx, 1, lbl, font=BLD_FONT)
                    existing[lbl] = row_idx
                sc(ws, row_idx, 2, data['fawen'])
                sc(ws, row_idx, 3, data['tj'])
                sc(ws, row_idx, 4, data['yd'])
                c = ws.cell(row=row_idx, column=5, value=data['liuzhuan'])
                c.alignment = CENTER; c.border = BORDER
                c.number_format = '¥#,##0.00'
                print(f"  [{sheet_name}] {lbl}: 发文{data['fawen']} 推荐{data['tj']} 阅读{data['yd']} 流转¥{data['liuzhuan']:.2f}")
                d += timedelta(days=1)
            continue

        is_micro = '微头条' in sheet_name
        ctype    = 3 if is_micro else 1

        # 把旧列名"批"改成"号"
        for c in range(1, ws.max_column + 1):
            h = ws.cell(1, c).value
            if h and isinstance(h, str) and '批' in h:
                ws.cell(1, c).value = h.replace('批', '号')

        # 读现有发布日行
        existing = {}
        for r in range(2, ws.max_row + 1):
            lbl = ws.cell(r, 1).value
            if lbl: existing[str(lbl)] = r

        # 只追加昨天（stat_date-1）那一行（如果不存在）
        if pub_label not in existing:
            new_row = ws.max_row + 1
            sc(ws, new_row, 1, pub_label, font=BLD_FONT)
            existing[pub_label] = new_row
            print(f"  [{sheet_name}] 新增行: {pub_label}")

        # 检查今天统计列是否已存在
        headers = [ws.cell(1, c).value for c in range(1, ws.max_column + 1)]
        col_check = f"{stat_day}阅读" if is_micro else f"{stat_day}推荐"
        if col_check in headers:
            print(f"  [{sheet_name}] {stat_day} 列已存在，跳过")
            continue

        # 追加今天的统计列
        if is_micro:
            col = ws.max_column + 1
            sc(ws, 1, col, f"{stat_day}阅读", NEW_FILL, WHT_FONT)
            ws.column_dimensions[get_column_letter(col)].width = 11
        else:
            rec_col  = ws.max_column + 1
            read_col = ws.max_column + 2
            sc(ws, 1, rec_col,  f"{stat_day}推荐", NEW_FILL, WHT_FONT)
            sc(ws, 1, read_col, f"{stat_day}阅读", NEW_FILL, WHT_FONT)
            ws.column_dimensions[get_column_letter(rec_col)].width = 11
            ws.column_dimensions[get_column_letter(read_col)].width = 11

        # 拉各发布日数据填入
        for pub_lbl, row_idx in sorted(existing.items(), key=lambda x: x[0]):
            d = parse_date_label(pub_lbl)
            if d is None or d > stat_date: continue
            data = fetch_day(cookies, d, ctype)
            print(f"    {pub_lbl}: 发文{data['total']} 推荐{data['recommend']} 阅读{data['read']}")
            val_rec  = data['recommend'] or '-'
            val_read = data['read'] or '-'
            if is_micro:
                sc(ws, row_idx, col, val_read)
            else:
                sc(ws, row_idx, rec_col,  val_rec)
                sc(ws, row_idx, read_col, val_read)
            if ws.cell(row_idx, 2).value in (None, 0, '-', ''):
                sc(ws, row_idx, 2, data['total'])

    wb.save(XLSX_PATH)
    print(f"\n已保存: {XLSX_PATH}")

def main():
    today = date.fromisoformat(sys.argv[1]) if len(sys.argv) > 1 else date.today()
    print(f"统计日: {today}  ({today.day}号列)\n")

    print("读取小馆cookie...")
    xg = load_cookies_sqlite()
    print(f"  {'OK' if xg.get('sessionid') else '失败'}")
    print("读取迦境cookie（罐头需开着）...")
    jj = load_cookies_cdp()
    print(f"  {'OK' if jj.get('sessionid') else '失败'}\n")

    append_to_xlsx(today, xg, jj)
    print("完成！")

if __name__ == '__main__':
    main()
