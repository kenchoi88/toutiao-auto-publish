---
name: Win 高 DPI 缩放鼠标偏移修复 (dpi_fix.py 跨机方案, 阿良 2026-05-18)
description: "Win 11 25H2 默认非 100% 缩放 → 罐头 webview 与 Python win32api.SetCursorPos 坐标系不一致 → 鼠标点不到按钮 → 发文失败.  dpi_fix.py 注册表读真 DPI + 环境变量开关跨机统一."
type: feedback
---

# 规则

跨机部署罐头自动发布时, 三大件主脚本(gtg_batch.py / gtg_timer.py) 顶部应
`import dpi_fix`. dpi_fix.py 默认 no-op, **仅当环境变量 `DPI_FIX_ENABLE=1`** 时激活
monkey patch `win32api.SetCursorPos` 按真实 DPI 倍率缩放.

新机部署 (Win 11 非 100% 缩放):
```cmd
setx DPI_FIX_ENABLE 1
```
→ 永久启用. mac 上 / 老机 100% 缩放不设, dpi_fix 自动跳过.

# Why

**症状**: 新台机 (kenchoiwinmini @ Win 11 Pro 25H2, 150% 缩放) 跑文章自动发布
报 "X 发布失败: 找不到文档导入按钮". 老台机 (125% 缩放) 同款脚本能跑.

**根因 (阿良 2026-05-18 凌晨 CDP 实证)**:
1. 罐头 (Electron) DPI aware, webview 看到 `devicePixelRatio=1.5`, CSS 像素 ≠ 物理像素
2. 脚本拿 webview JS 的 CSS 坐标 (例 108,459) + window.screenX/Y (CSS)
3. 脚本传给 `win32api.SetCursorPos((x, y))` —— 但**SetCursorPos 接收物理坐标**
4. CSS 坐标 < 物理坐标 (150% 下差 1.5 倍) → 鼠标飞到偏左上 → 没点中"发布文章"按钮
5. webview 从未真正切到编辑器页面 → `.syl-toolbar-button` 永远 0 → 报 timeout

**为什么老台机能跑 (125% 也是非 100%)**: 未深查, 可能 win32api 在 125% 下偏移落差较小
能误中按钮; 或 Python 进程 DPI awareness 状态跟新台机不同. 无论如何 dpi_fix
跨机一致 + 环境变量开关 = 安全.

**为什么 Python `GetDeviceCaps(88)` 假报 96**:
Win 8+ 对 DPI Unaware 进程虚拟化 DPI, GetDpiForSystem / GetDpiForWindow /
GetDeviceCaps 全部返回 96, 让 unaware 进程以为自己在 100% 缩放屏幕.
**真实 DPI 必须读注册表** `HKCU:\Control Panel\Desktop\WindowMetrics\AppliedDPI`.

# How to apply

## 1. dpi_fix.py 完整内容 (跨机一致, 写到 gtg_batch.py 同目录)

```python
# dpi_fix.py v3 — 阿良 2026-05-18 — Win 高 DPI 缩放修复
# 默认 no-op (跨机代码 100% 一致, 不影响老台机/Mac)
# 仅当环境变量 DPI_FIX_ENABLE=1 时激活 (新台机 setx 永久启用)
import sys, os

if sys.platform == 'win32' and os.environ.get('DPI_FIX_ENABLE') == '1':
    import ctypes
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(2)
    except Exception:
        try: ctypes.windll.user32.SetProcessDPIAware()
        except Exception: pass

    SCALE = 1.0
    DPI = 96
    SOURCE = 'default'
    try:
        import winreg
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Control Panel\Desktop\WindowMetrics') as k:
            DPI, _ = winreg.QueryValueEx(k, 'AppliedDPI')
            SCALE = DPI / 96.0
            SOURCE = 'registry'
    except Exception:
        try:
            hdc = ctypes.windll.user32.GetDC(0)
            DPI = ctypes.windll.gdi32.GetDeviceCaps(hdc, 88)
            ctypes.windll.user32.ReleaseDC(0, hdc)
            SCALE = DPI / 96.0
            SOURCE = 'GetDeviceCaps'
        except Exception:
            pass

    if SCALE != 1.0:
        try:
            import win32api
            _orig = win32api.SetCursorPos
            def _scaled(pos):
                _orig((int(pos[0] * SCALE), int(pos[1] * SCALE)))
            win32api.SetCursorPos = _scaled
            sys.stderr.write(f"[dpi_fix] SetCursorPos *={SCALE} (DPI={DPI}, source={SOURCE})\n")
        except Exception as e:
            sys.stderr.write(f"[dpi_fix] patch failed: {e}\n")
else:
    SCALE = 1.0
    DPI = 96
    SOURCE = 'disabled'
```

## 2. 主脚本顶部加 import

`gtg_batch.py` / `gtg_timer.py` 第一行 `import` 之前插入:
```python
import dpi_fix  # [v1103] Win 高 DPI 2026-05-18 阿良 (默认 no-op, 需 setx DPI_FIX_ENABLE=1)
```

## 3. 新机激活 (仅 Win + 非 100% 缩放)

```cmd
setx DPI_FIX_ENABLE 1
```
(setx 写 HKCU:\Environment, 永久. 当前 shell 不生效, 下次 Python 启动才继承)

## 4. 验证

```cmd
python -c "import dpi_fix; print('SCALE=', dpi_fix.SCALE, 'SOURCE=', dpi_fix.SOURCE)"
```

期望:
- 新台机 (150% 缩放, env=1): `SCALE= 1.5 SOURCE= registry` + stderr `[dpi_fix] SetCursorPos *=1.5 ...`
- 老台机 (125% 缩放, env 未设): `SCALE= 1.0 SOURCE= disabled`
- mac 任何机: `SCALE= 1.0 SOURCE= disabled`

# 跨机一致性原则 (阿良铁则)

- **代码 100% 一致**: 所有 Win 同 dpi_fix.py + import, 所有 Mac 同 (mac 上直接跳过)
- **行为按环境变量决定**: 每机 setx 独立, 不入仓库, 不入代码
- **新机部署只需一行 setx**: 部署文档/搬家方案直接写

# 部署历史

- 2026-05-18 凌晨: 新台机 setx 启用 + 文章自动发布**顺利发布** ✓
- 2026-05-18 凌晨: 老台机部署 dpi_fix.py + import, 未设环境变量 (保持原行为)
- 2026-05-18: 推入仓库 `自动发布/自动发布V1103/{微头条,文章,文章定时}/{mac,win}/`

# 引用

- [[reference_新台机kenchoiwinmini_打通通道]] — 同晚立, 含 SSH/Python/Tailscale 配置
- 自动发布/故障说明/故障说明_2026-05-18.txt — 同晚故障说明
