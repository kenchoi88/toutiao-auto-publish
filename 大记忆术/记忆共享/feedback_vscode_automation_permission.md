---
name: VSCode自动化权限正确开放方法
description: macOS弹出VSCode权限弹窗的正确触发方式，阿良绝对不能搞反
type: feedback
originSessionId: 6d1e89eb-eddc-422c-b35c-b420271a3a68
---
**必须让用户在VSCode的Terminal窗口里亲自运行这条命令：**

```bash
osascript -e 'tell application "创作罐头" to activate'
```

macOS弹出"Visual Studio Code 想访问其他 App 的数据"，用户点允许，永久搞定。

**Why:** macOS识别权限发起方是父进程（VSCode），必须从VSCode Terminal里触发，才能让权限绑定到VSCode。从我（Claude/终端其他位置）触发是无效的，绑定对象不对，下次照样弹。

**How to apply:** 我不能替用户触发这个，只能告诉用户在VSCode Terminal里自己跑上面那条命令。不要自作主张从自己这边触发，那是无效的，会让缺哥觉得搞定了但实际没搞定。

系统大版本更新后权限可能重置，重置后让用户重跑一次即可。
