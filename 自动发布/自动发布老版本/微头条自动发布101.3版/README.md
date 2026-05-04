# 微头条自动发布 v1101.3 — 头条首发"取消勾选"假动作 hotfix

## 修的 BUG
publish_article() 里 should_first=False 时执行的"取消勾选"是空点 —
JS 返的是"头条首发"四个字 textNode 的 boundingClientRect 中心,
不是复选框 input 的真坐标。win32 真鼠标点到文字上,cb.checked 不变;
脚本却照打 "头条首发: 取消勾选 (sx,sy)" 看着每次都成功,实际一次没切换。
点完也无回读校验。

## 实战证据(被截图样本号 04-17 ~ 04-28)
9 次首发审核违规通知,内容均"非原创",每次扣 5 分:
- 04-17 拉夫罗夫 / 04-18 界面快讯 / 04-20 沙特 / 04-21 日本战舰 /
  04-22 台湾国防部 / 04-25 崩老头 / 04-25 米线馆 / 04-26 泽连斯基 / 04-28 德黑兰
累计扣 45 分,从 100 → 55,29 号 12:10 触发 <60 硬终止漏发 5 名额。
群体性号信用分下滑(29 号 697 次读取里 ≥95 仅 19 次,2.7%)。

## 修法(三大件 win/ 同段统一 patch)
1. JS 探测改返回 cb (input[type=checkbox] / role=checkbox) 自身中心坐标,
   cb 宽高 <4 退而求次取可见父节点矩形。
2. 真鼠标点击后 sleep 0.4s 重读 isChecked,与 should_first 比对。
3. 不一致 → 重试一次真鼠标 → 仍不一致 → 降级 JS cb.click() +
   dispatchEvent('change',{bubbles:true}) 兜底。
4. 三轮全失败时:
   - 应取消但仍勾着 → ★ 硬保护:wsc.close() return False("首发取消失败(硬保护)")
     本篇不发,避免被扣 5 分。
   - 应勾未勾 → 继续发(只是失去首发激励,不会被扣)。
5. 日志区分 "已校验" / "校准失败" / "硬保护跳过",便于审计。

## 落地状态
- ✓ win  — 绣虎落(2026-04-29);桌面三大件已同步
- ☐ neo  — 小齐 + 小师弟待落 (mac/gtg_batch.py)
- ☐ air  — 阿良待落 (mac/gtg_batch.py)
- ☐ mini — 东山待落 (mac/gtg_batch.py)
- ☐ neo2 — 左右待落 (mac/gtg_batch.py)

Mac 端代码框架略不同(用 account_name 不是 name),
参考 win/gtg_batch.py 1737-1840 段思路自行同步。

## 目录
- `win/gtg_batch.py` — 已 patch v1101.3
- `win/go.bat` — 沿用
- `mac/gtg_batch.py` — **暂留 v1101.2 旧版,等各 Mac Claude 上 v1101.3**

## 上线后观察(48 小时)
- 不再有"首发审核非原创"扣分通知 → 修复成功(UI 复选框未真切换是根因)
- 仍有 → B 假说成立(账号已注册"首发激励计划",平台审核与 UI 复选框无关),
  需在头条创作者后台手工退出"首发激励计划"才能彻底关掉首发审核。
