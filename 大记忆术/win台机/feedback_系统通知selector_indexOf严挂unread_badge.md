---
name: feedback-selector-indexof-unread-badge
description: "check_system_notice 的 conversation tab click selector — win 端 indexOf(\"...\") === 0 在 unread badge 数字顶到 0 位时不命中, 必须 !== -1 跟 mac 同款 V1102.9-mac-fix (2026-05-19 老台机/air 双频道实证)"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: d42ef16d-8751-413e-8cd0-08a6b1f215d0
---

# check_system_notice selector 必须 indexOf !== -1 (不能 === 0)

[gtg_batch.py:1170 win / 1179 mac] check_system_notice 函数 click conversation tab:
```js
var items = document.querySelectorAll('.conversation-box.notify-im-user-item');
for(var i=0; i<items.length; i++){
    var t = (items[i].innerText || '').trim();
    if(t.indexOf("{channel_json}") !== -1){   // ★必须 !== -1, 不能 === 0
        items[i].click();
        return 'ok';
    }
}
```

**Why:**
罐头消息中心 conversation item innerText 是拼接结构 `"<unread_badge>\n<channel_name>\n<time>\n<preview>"`. 当 conversation 有未读消息时, unread badge(数字)会**顶到 0 位**, 例如:
- 无未读: `"系统通知\n05-18 16:11\n亲爱的创作者..."` → indexOf("系统通知") = **0** ✓
- 有未读: `"1\n系统通知\n05-18 16:11\n亲爱的创作者..."` → indexOf("系统通知") = **2** ✗

→ `=== 0` 永远漏掉**有未读的 conversation** (而那正是需要 click 进去读的). 必须放宽 `!== -1`.

mac 端 V1102.9-mac-fix 早就发现并改了, 注释明确写 `[v1102.9-mac-fix] indexOf===0 太严, unread badge 数字会顶到 0 位; 放宽 includes`. **win 端漏同步**, 直到 2026-05-19 缺哥跑「幸福圈」实证「未找到频道: 系统通知」才暴露.

**How to apply:**
- 改 check_system_notice 的 conversation click selector 时, 严禁用 indexOf === 0. 死规则: 用 `!== -1` (跟 mac 同款).
- 同款规则适用任何**针对带 unread badge UI 元素的 selector**: 列表项 innerText 拼接里 badge 永远在前.
- 不要 over-engineer 改成真鼠标 cliclick / win32api (2026-05-19 绣虎试过, 缺哥纠正"JS click 本身就 work, 不模拟鼠标也能命中, 别折腾"). JS items[i].click() 在 conversation tab 切换上是 work 的, 平台不需要 isTrusted=true.

## 实证 (2026-05-19 老台机 + air 双机各跑 1 篇)

```
老台机 幸福圈     [01:06:45] ⚠ 系统通知 1 条 → 系统通知.txt (5/18 16:11 侵犯名誉投诉)
老台机 青墨染流年 [01:08:56] ⚠ 审核通知 1 条 → 审核通知.txt (首发不符扣 5 分)
air   暗夜行者之光 [01:20:55] ⚠ 系统通知 1 条 → 系统通知.txt (5/18 11:10 侵犯名誉投诉)
```

全部命中, 没"未找到频道", 不再串入活动通知.

## 落地

- 老台机桌面 微头条/gtg_batch.py: line 1170 `=== 0 → !== -1`
- 新台机桌面 微头条/gtg_batch.py: line 1170 (含 import dpi_fix + zoom 动态 patch 后) `=== 0 → !== -1`
- 仓库 V1103/win/gtg_batch.py: 同 (commit `e54b18f`)
- 仓库 V1103/mac/gtg_batch.py: V1102.9-mac-fix 原版已 `!== -1`, 不动
- 4 mac 桌面 微头条/gtg_batch.py: V1103 大统一时就同 mac 版 `!== -1`, 不动 (grep 实证)

## 相关

- [[reference_罐头CDP嵌套结构与坐标链]] — 罐头消息中心 webview 嵌套结构
- [[feedback_WIN_MAC不可跨推]] — win/mac 是两条独立线, mac-fix 不会自动同步到 win
- [[feedback_真鼠标点击_勿换CDP]] — cliclick / win32api 真鼠标是反风控冗余, 但**对 conversation tab 切换不需要**, JS click 够用
- 故障说明_2026-05-19.txt
- gtg_batch.py:1163-1186 — check_system_notice channel click 段
