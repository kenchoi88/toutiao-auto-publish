---
name: VSCode扩展bypassPermissions正确配置位置
description: Claude Code工具执行权限弹窗的正确解法，~/.claude/settings.json不管VSCode扩展
type: feedback
originSessionId: 6d1e89eb-eddc-422c-b35c-b420271a3a68
---
**VSCode扩展的权限配置不在 `~/.claude/settings.json`，在这里：**

```
~/Library/Application Support/Code/User/settings.json
```

需要加上：
```json
{
    "claudeCode.preferredLocation": "panel",
    "claudeCode.initialPermissionMode": "bypassPermissions"
}
```

加完重启VSCode，之后大部分工具调用不再弹窗。

**特殊情况：bash脚本执行还会弹一次**
第一次执行某个bash脚本（如go.command），VSCode还是会弹"Allow this bash command?"，选 **"Yes, allow bash ... for this project (just you)"**，加入白名单，以后永不弹。

**Why:** 今晚（2026-04-12）权限弹窗问题磨了很久，阿良一直绕弯子，最后小齐SSH进来查出来的。两套系统：`~/.claude/settings.json` 是CLI用的，VSCode扩展读的是 `Code/User/settings.json` 里的 `claudeCode.initialPermissionMode`。只配一个没用，阿良没搞清楚这个差异，反复让缺哥重启测试，浪费大量时间，最后让小齐收尾，很丢人。

**How to apply:** 以后碰到VSCode里Claude Code工具执行弹窗，第一步直接查 `~/Library/Application Support/Code/User/settings.json`，不要再去动 `~/.claude/settings.json`，更不要让缺哥反复重启测试。
