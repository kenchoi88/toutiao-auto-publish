---
name: 罐头账号筛选标签 CDP+cliclick 自动化
description: 用 CDP+cliclick 自动操作罐头侧边栏"账号筛选"弹窗的完整流程与5个踩坑教训
type: reference
---

# 罐头账号筛选标签 CDP+cliclick 自动化

罐头侧边栏顶部的"账号筛选"弹窗（漏斗图标）控制了侧边栏显示哪些账号。
脚本的 `collect_accounts` / `scroll_find_account` 都依赖侧边栏当前显示状态，
所以**筛选状态不对会导致脚本扫不到部分账号**——给 txt 名单也救不了。

阿良 2026-04-30 在 air 本机完整跑通自动化操作筛选弹窗的流程，沉淀如下。

## 完整流程（7 步）

```python
# 1. 罐头窗口拿前台 + AXRaise(必不可少,否则弹窗不渲染)
osascript: tell application "创作罐头" to activate
            tell process "创作罐头" to set frontmost to true
            try: tell window 1 to perform action "AXRaise"
sleep 1.0

# 2. cliclick 真鼠标点漏斗按钮(屏幕坐标=window.screenX+CSS坐标)
btn_dom = JS: document.querySelector('[class*="tabsFilterIcWarpper"]')
btn_screen_x = window.screenX + btn_rect.left + btn_rect.width/2
btn_screen_y = window.screenY + btn_rect.top + btn_rect.height/2
cliclick c:btn_screen_x,btn_screen_y
sleep 1.0

# 3. 验证弹窗真打开(DOM + 计算样式)
panel = JS: document.querySelector('[class*="tabsFilterPopover"]')
panel.computedStyle.display !== 'none' && getBoundingClientRect.width > 100

# 4. 清空已选标签:连续 cliclick 同一坐标(close 按钮自动滑过来)
loop:
    closes = JS: panel.querySelectorAll('[class*="arco-tag"] [class*="close"]')
    if !closes.length: break
    cliclick c:closes[0].screen_x,closes[0].screen_y  # air 实测=(1337,350)
    sleep 0.8

# 5. 点开"全部标签"select(arco-select-multiple)
tag_select = JS: panel 内 textContent 含"标签"或"批"的 arco-select
cliclick c:tag_select.screen_x,tag_select.screen_y  # air 实测=(1369,350)
sleep 1.0

# 6. 下拉浮层渲染后,逐个 cliclick 选项(每次重读 DOM 取最新坐标)
for target in TARGETS:
    pos = JS: arco-select-popup 内 textContent === target 的选项
    if pos.already_selected: skip
    pos.scrollIntoView({block:'center', behavior:'instant'})
    cliclick c:pos.screen_x,pos.screen_y
    sleep 0.5

# 7. 关弹窗 + 验证侧边栏账号数量到位
JS: document.body.click()
sleep 0.5
扫侧边栏 .account-RALrbJ 应得到期望数量
```

## 5 个技术坑（必须沉淀，后续 agent 别重踩）

### 坑 ① JS click() 触发 React 组件无效

`btn.click()` / `dispatchEvent('click')` 在 React 受控组件上**不会**让弹窗弹出来——
isTrusted 检查拦截了所有合成事件。

→ **必须用 cliclick 真鼠标** 或 CDP `Input.dispatchMouseEvent`（后者是浏览器级注入，算"真"事件）。

### 坑 ② CDP dispatchMouseEvent 算真事件，但弹窗渲染依赖罐头是否在前台

CDP `Input.dispatchMouseEvent` 能让 React 收到点击事件、DOM 状态会改，
但**罐头被其他窗口遮挡时屏幕不渲染弹窗**——你 dump DOM 看到 popover visible，
但屏幕上肉眼看不到，后续依赖该 DOM 的操作可能错位。

→ 必须 `osascript activate + set frontmost to true + AXRaise` 三件套，把罐头真推到前台。
   推完之后用 cliclick 真鼠标更稳（dispatchMouseEvent 可作为补充手段）。

### 坑 ③ arco-tag X 关闭按钮重叠特性

连续 X 三个标签时，每次 X 完后剩余标签向左挤，**下一个 X 按钮会滑到固定屏幕坐标**
（air 实测 `(1337, 350)`，台机/mini/neo 因窗口位置不同坐标各异，但同机器内一致）。

可以连续 cliclick 同一坐标 N 次实现批量清空，无需重新读 DOM 取坐标。

### 坑 ④ arco-select 多选超过 2 个会折叠成 "+1..."

验证已选标签数量时，**不要靠数 `[class*="arco-tag"]` 的 close 按钮**——多于 2 个时
超出部分进 `+1...` 折叠，没有可见的 close 按钮。

→ 验证用 select 的 textContent（会显示前 2 个+"+1..."），
  或更直接：扫侧边栏 `.account-RALrbJ` 数量是否到达期望值。

### 坑 ⑤ 下拉浮层选项每次点选后会重渲染

浮层里逐个点选目标标签时，**每选一个就要重新读浮层 DOM 拿当前剩余选项坐标**——
不能一次性缓存所有目标坐标连点（选过的会变 `selected`，DOM 排序可能变，新坐标不准）。

→ 循环里每次重新 `JS querySelectorAll arco-select-option` 取目标。

## 关键 DOM 选择器速查

| 组件 | 选择器 |
|---|---|
| 漏斗按钮 | `[class*="tabsFilterIcWarpper"]` |
| 筛选弹窗 popover | `[class*="tabsFilterPopover"]` |
| 弹窗内 select 多选 | 弹窗内 `[class*="arco-select"][class*="multiple"]` |
| 已选标签 chip | 弹窗内 `[class*="arco-tag"]` |
| 标签 X 按钮 | tag 元素内 `[class*="close"]` |
| 下拉浮层 | `[class*="arco-select-popup"]`（顶层 document 下，不在弹窗内） |
| 浮层选项 | 浮层内 `[class*="arco-select-option"]` |
| 清除筛选按钮 | 弹窗内 textContent === "清除筛选" |
| 侧边栏账号 | `.account-RALrbJ` |
| 侧边栏滚动容器 | `[class*="menuMainWarpper"]` |

## 屏幕坐标算法（统一）

```javascript
JS: var rect = el.getBoundingClientRect();
    screen_x = window.screenX + rect.left + rect.width / 2;
    screen_y = window.screenY + rect.top + rect.height / 2;
```

主窗口 frame 的 `window.screenX/Y` 直接对应窗口在屏幕上的视口左上角，
不需要补偿菜单栏（macOS）或标题栏。这跟 webview 内点击算法一致。

## 何时用这套自动化

**适合**：脚本启动前一次性配置筛选标签（无人值守前置步骤）。

**不适合**：脚本运行中调用——cliclick 是真鼠标，会抢用户光标 0.5-2 秒，
任何同时操作的人或并行进程都会被打断。

## 相关故障记录

- 故障日志.txt: `[2026-04-30 17:00] [台机/全队] 漏扫账号 — 标签贴漏导致 collect_accounts 偏差`
- 版本说明.txt: 「待并入 v1102 — 账号筛选标签 CDP+cliclick 自动化」
