# 文章定时自动发布 v1101.3 — 头条首发"取消勾选"假动作 hotfix

## 修的 BUG
publish_article() 里 should_first=False 时执行的"取消勾选"是空点 —
JS 返的是"头条首发"四个字 textNode 的 boundingClientRect 中心,
不是复选框 input 的真坐标。win32 真鼠标点到文字上,cb.checked 不变;
脚本却照打 "头条首发: 取消勾选 (sx,sy)" 看着每次都成功,实际一次没切换。
点完也无回读校验。

详见微头条 v1101.3 README。三大件 win/ 同段同 bug,同 patch。

## 修法(同微头条 v1101.3)
1. JS 改返回复选框 input 自身坐标,不是文字坐标
2. 真鼠标点击后 0.4s 回读 isChecked 校验
3. 不一致 → 重试 → JS cb.click() 兜底
4. 三轮全失败 + 应取消仍勾 → ★ 硬保护跳过该篇,避免被扣 5 分

## 落地状态
- ✓ win  — 绣虎落(2026-04-29);桌面已同步
- ☐ Mac 4 机 — 各 Claude 自行同步(代码框架略不同,用 account_name;
  其中文章定时 mac 走 gtg_timer.py)

## 目录
- `win/gtg_timer.py` — 沿用(定时排程核心,不涉及首发逻辑)
- `win/gtg_batch.py` — 已 patch v1101.3(发文核心)
- `win/go.bat` — 沿用
- `mac/gtg_timer.py` — **暂留 v1101.2 旧版,首发逻辑同 bug**
