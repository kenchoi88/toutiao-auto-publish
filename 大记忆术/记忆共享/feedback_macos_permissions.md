---
name: macOS辅助功能和自动化权限开启方法
description: 辅助功能必须手动勾终端；自动化权限空白时需先触发一次才会出现
type: feedback
originSessionId: 0e9e6cdf-de45-458d-b2ce-c21a71bbed5d
---
**规则：macOS权限只说中文，叫"终端"不叫"Terminal"。**

**Why:** 用户要求说中文，"Terminal"让用户困惑。

**How to apply:** 提到macOS权限时一律说"终端"。

---

**辅助功能**：系统设置 → 隐私与安全性 → 辅助功能 → 勾上"终端"

**自动化权限空白**：不是问题，自动化权限需要先触发一次才会出现。让用户双击go.command，弹出权限询问点"好"，之后自动化里就有了。

**Why:** 自动化权限是按需注册的，首次触发才会出现在列表里。

**How to apply:** 用户说自动化空白时，告诉他双击脚本触发一次即可，不是bug。
