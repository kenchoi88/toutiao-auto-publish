# 文章定时自动发布 v1101.2 — 末位账号 CDP 注入彻底修复

## 修复内容
v1101 scroll_find_account 搜索框 fallback 把 cliclick + osascript keystroke
替换成 CDP nativeInputValueSetter JS 注入。绕过键盘焦点 + 罐头前台依赖。

## 实战印证(air, 2026-04-29 凌晨)
同微头条 v1101.2:海屿星辰末位账号 4 大循环死磕 → 注入后一次命中,295→300 全发完。

## 落地状态
- ✓ neo  — 小齐落(2026-04-29)
- ✓ air  — 阿良落(2026-04-29)
- ✓ win  — 绣虎之前已落桌面真版(本目录 win/ = 桌面 cp)
- ☐ mini — 东山待落
- ☐ neo2 — 左右待落

## 目录
- `win/gtg_timer.py` — 从 Win 台机桌面真版 cp(定时排程核心)
- `win/gtg_batch.py` — 从 Win 台机桌面真版 cp(发文核心,已含 CDP 注入 + 关 tab 重建 partition L2 兜底)
- `win/go.bat` — 启动脚本(沿用 v1101.1)
- `mac/README.md` — 占位,待 air + neo 推桌面真版后绣虎合
