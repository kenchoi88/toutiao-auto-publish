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
