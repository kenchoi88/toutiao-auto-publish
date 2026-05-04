#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""5 机 × 3 件 账号配置.xlsx 结构对齐 — 加缺失 sheet + 统一列名,不动数据"""
import sys, os, shutil
from datetime import datetime
sys.stdout.reconfigure(encoding='utf-8')
import openpyxl

# 标准 7 sheet + 列定义
STANDARD = [
    ('不首发',     ['账号名']),
    ('永久跳过',   ['账号名']),
    ('本轮已发',   ['账号名', '已发次数']),
    ('白名单',     ['账号名', '发文份数']),
    ('失败列表',   ['账号名', '失败原因', '文稿名', '失败时间', '轮次']),
    ('硬终止账号', ['账号名', '终止原因', '终止时间', '本次已发篇数']),
    ('发文汇总',   ['账号名', '轮次', '发文时间', '失败时间', '补发成功时间']),
]

if len(sys.argv) < 2:
    print("用法: python script.py <账号配置.xlsx>"); sys.exit(1)
fp = sys.argv[1]
if not os.path.exists(fp):
    print(f"FILE_NOT_FOUND: {fp}"); sys.exit(1)

ts = datetime.now().strftime("%Y%m%d_%H%M%S")
bak = f"{fp}.bak_pre_align_{ts}"
shutil.copy(fp, bak)

wb = openpyxl.load_workbook(fp)
changes = []

for sheet_name, cols in STANDARD:
    if sheet_name not in wb.sheetnames:
        ws = wb.create_sheet(sheet_name)
        for c, name in enumerate(cols, 1):
            ws.cell(row=1, column=c, value=name)
        changes.append(f"+加 sheet [{sheet_name}]")
    else:
        ws = wb[sheet_name]
        for c, name in enumerate(cols, 1):
            cur = ws.cell(row=1, column=c).value
            if cur != name:
                ws.cell(row=1, column=c, value=name)
                changes.append(f"  [{sheet_name}] 列{c}: {repr(cur)} → {repr(name)}")

if changes:
    wb.save(fp)
    print(f"  [{fp}]")
    for c in changes: print(f"    {c}")
    print(f"    备份: {bak}")
else:
    print(f"  [{fp}] 已对齐, 无改动")
    os.remove(bak)
