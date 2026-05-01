#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
catchup.py — 中断恢复一键工具(三大件通用)
2026-05-02 沉淀于凌晨电信断网事件后,缺哥拍板。

用法:
    cd ~/Desktop/<件>自动发布 && python3 catchup.py

逻辑:
    1. 自适应当前所在件类型(微头条/文章)
    2. 找文章定时件「待补漏」sheet(权威数据源)
    3. 从最近 log 抽断点账号(最后一篇 ✓ 定时发布成功 的下一个)
    4. 环形重排:断点为首 → 末 → 绕回开头
    5. 写本件「白名单」+ 备份原 xlsx
    6. 报告:断点 / 待补总数 / 首位末位

部署位置:
    - 5 机各自的 ~/Desktop/{微头条,文章}自动发布/catchup.py
    - Win 台机:~/Desktop/台机专用自动发布/{微头条,文章}自动发布/catchup.py
"""
import os, sys, glob, shutil, time, re
from pathlib import Path

try:
    from openpyxl import load_workbook
except ImportError:
    print("缺 openpyxl: pip install openpyxl"); sys.exit(1)

HERE = Path(__file__).parent.resolve()
HOME = Path.home()


def detect_kind():
    n = HERE.name
    if "微头条" in n: return "微头条"
    if "文章" in n:   return "文章"
    print(f"✗ 未识别件类型 (HERE={HERE.name})"); sys.exit(1)


def find_timer_dir():
    """找文章定时件目录(各机命名差异)"""
    cands = [
        HOME / "Desktop/文章定时自动发布",
        HOME / "Desktop/Mac文章定时自动发布",
        HOME / "code/头条自动发布/文章定时自动发布",
        HOME / "code/头条自动发布/Mac文章定时自动发布",
        HOME / "Desktop/台机专用自动发布/文章定时自动发布",  # Win 台机
    ]
    for d in cands:
        if d.exists() and (d / "账号配置.xlsx").exists():
            return d
    return None


def read_待补漏(timer_dir):
    p = timer_dir / "账号配置.xlsx"
    try:
        wb = load_workbook(p, read_only=True, data_only=True)
        if "待补漏" not in wb.sheetnames:
            wb.close(); return []
        ws = wb["待补漏"]
        items = []
        for r in range(2, ws.max_row + 1):
            name = ws.cell(r, 1).value
            miss = ws.cell(r, 2).value
            if name and miss:
                try:
                    m = int(miss)
                    if m > 0:
                        items.append((str(name).strip(), m))
                except (ValueError, TypeError):
                    pass
        wb.close()
        return items
    except Exception as e:
        print(f"  ! 读「待补漏」失败: {e}")
        return []


def find_breakpoint(items, timer_dir):
    """从 文章定时件 最新 log 找最后一篇 ✓ 定时发布成功 的账号 → 返回 它在 items 中的下一个 index"""
    if not items or not timer_dir: return 0
    log_root = timer_dir / "运行报告"
    if not log_root.exists(): return 0
    logs = sorted(log_root.glob("*/运行日志.txt"), key=lambda p: p.stat().st_mtime, reverse=True)
    if not logs: return 0

    last_account = None
    pat = re.compile(r"✓ 定时发布成功:\s*(.+)")
    try:
        with open(logs[0], encoding="utf-8") as f:
            for line in f:
                m = pat.search(line)
                if m:
                    last_account = m.group(1).strip()
    except Exception as e:
        print(f"  ! 读 log 失败: {e}")
        return 0

    if not last_account:
        return 0
    names = [n for n, _ in items]
    if last_account not in names:
        # 最后成功账号已被清出待补漏(它本来就发完了)— 起点用 items 第一个
        return 0
    idx = names.index(last_account)
    return (idx + 1) % len(items)


def write_whitelist(items, start_idx):
    p = HERE / "账号配置.xlsx"
    if not p.exists():
        print(f"✗ 当前件无 账号配置.xlsx: {p}"); sys.exit(1)
    ts = time.strftime("%Y%m%d_%H%M%S")
    bak = str(p) + f".bak_catchup_{ts}"
    shutil.copy2(p, bak)
    print(f"备份: {os.path.basename(bak)}")

    ordered = items[start_idx:] + items[:start_idx]

    wb = load_workbook(p)
    if "白名单" not in wb.sheetnames:
        ws = wb.create_sheet("白名单")
        ws.cell(1, 1, "账号名"); ws.cell(1, 2, "发文份数")
    else:
        ws = wb["白名单"]
        if ws.max_row >= 2:
            ws.delete_rows(2, ws.max_row - 1)
    r = 2
    for name, miss in ordered:
        ws.cell(r, 1, name); ws.cell(r, 2, miss); r += 1
    wb.save(p)

    total = sum(m for _, m in ordered)
    print(f"✓ 白名单 {r-2} 行 / 共 {total} 篇待补")
    print(f"  首位(断点): {ordered[0][0]}  漏 {ordered[0][1]} 篇")
    print(f"  末位:         {ordered[-1][0]}  漏 {ordered[-1][1]} 篇")


def main():
    kind = detect_kind()
    print(f"=== catchup.py · 件: {kind}自动发布 ===")
    print(f"    HERE: {HERE}\n")

    timer_dir = find_timer_dir()
    if not timer_dir:
        print("✗ 找不到 文章定时件 目录(待补漏 数据源)")
        print("  TODO: log fallback 模式未实现,人工写白名单")
        sys.exit(1)
    print(f"  文章定时件: {timer_dir}")

    items = read_待补漏(timer_dir)
    if not items:
        print("  ✗ 「待补漏」sheet 为空 — 文章定时件还没跑过 / 已被清空")
        print("    TODO: log fallback 算 quota - 已成功 (未实现)")
        sys.exit(1)
    print(f"  从「待补漏」读到: {len(items)} 账号 / {sum(m for _,m in items)} 篇待补")

    start_idx = find_breakpoint(items, timer_dir)
    if start_idx == 0:
        print(f"  断点: items[0] (找不到日志最后成功账号 / 或它已发完)")
    else:
        print(f"  断点: items[{start_idx}] = {items[start_idx][0]}")
    print()

    write_whitelist(items, start_idx)
    print()
    print("下一步: 双击 go.command (或 go.bat) 启动跑")


if __name__ == "__main__":
    main()
