# 4 mac Claude 上线手册

(缺哥串行做,共 air/mini/neo2 三台,~15 分钟)

## 已上线

- **neo (小齐)** ✓ 已登录,wrapper 实测通

## 待上线: air / mini / neo2

每台机操作完全一样,把下面 4 步在每台 mac 上**物理操作一次**(键盘启动 Terminal,不动鼠标,不打扰发文)。

## 单台 mac 操作流程(每台 ~5 min)

### 步骤 1: 在 mac 上打开 Terminal
```
Cmd+Space → 输 "terminal" → 回车
(键盘操作,别点桌面其他东西)
```

### 步骤 2: 在 Terminal 输 5 行(逐行回车)
```bash
export HTTPS_PROXY=http://127.0.0.1:1082
export HTTP_PROXY=http://127.0.0.1:1082
claude
```

会启动 Claude Code,**第一次启动会问主题选择**:
- 问 "Choose the text style" → 直接 Enter (默认 Dark mode)
- 问 "Allow Claude Code to..." 之类引导问 → 直接 Enter
- **直到看到 `>` 输入框出现**

### 步骤 3: 在 Claude Code 界面里输 /login
```
/login
```
回车后浏览器自动开 → Anthropic 授权页 → 点"授权"
浏览器显示 "You can close this window" → 关闭浏览器
回 Terminal,看到 "Login successful" 之类提示

### 步骤 4: 验证(两条命令)
```
退出 claude (Ctrl+C 或 /quit)
```

回到 zsh 提示符,输:
```bash
claude auth status
```
**期望看到**: `loggedIn: true`

如果是 `loggedIn: false` → 没真完成,重做步骤 3。

## 顺序建议

1. **air** 先做(这台路径特殊在 ~/wtt-go/,优先确认登录无路径影响)
2. **mini** 做
3. **neo2** 做

## 完成后告诉我

每台做完只需告诉我"air 好了" / "mini 好了" / "neo2 好了"。

我立即从台机 ssh + wrapper 测,贴回响应给你看。

## 我的测试命令

(缺哥不用做,我做):
```bash
CLAUDE_SSH_PWD=geng7997 python -X utf8 \
  c:/Users/kench/code/头条自动发布/会议室/scripts/claude_ssh.py \
  <机器> "你是谁?一句话答"
```

期望响应:
- **air (阿良)**: "我是阿良..." 之类
- **mini (东山)**: "我是东山..." 之类
- **neo2 (左右)**: "我是左右..." 之类

如果某台返回 "Not logged in" → 那台没真登录,缺哥重做步骤 3。

## 故障排查清单(出问题对照)

| 现象 | 原因 | 处理 |
|---|---|---|
| `command not found: claude` | Terminal 不是 login shell 或 PATH 有问题 | 退出再开 Terminal,或先 `source ~/.zshrc` |
| 浏览器开了但没回弹 Terminal | callback 端口被防火墙拦 | 等 30 秒,或重新 `/login` |
| `loggedIn: false` 但你点过"授权" | 授权没真完成 | 重新 `claude` → `/login` |
| 我 ssh 测仍 not logged in | Keychain 问题(你登录态在 GUI session) | 我 wrapper 已带 unlock,正常应通,不通找小齐诊断 |

## 4 mac 共用模板(放心,4 mac 流程完全一样)

不论 air/mini/neo2,**步骤 1-4 一字不差照做**。

差异点都在我 wrapper 端处理:
- 不同 mac 的 SSH 用户名(已写进 wrapper)
- 不同 mac 的 IP(已写进 wrapper)
- 不同 mac 的素材路径(发文相关,跟 claude CLI 无关)

## 不要做的事

- ❌ 不要在跑发文那个 Terminal 里跑 /login(开新 Terminal)
- ❌ 不要点桌面其他东西(动鼠标会打乱 cliclick 发文坐标)
- ❌ 不要 pkill claude(会杀掉 VSCode 内的 IDE 实例)
- ❌ 不要在 zsh 里输 `/login`(`/login` 是 Claude Code 交互界面里的命令,不是 zsh 命令)

## 准备好就做

去 air → mini → neo2,串行做。
做完任一台告诉我,我就开始测。
3 台都通后,我们开第二场会议(议题四 / 或议题待定 / 或继续议题二三 hook 落地讨论)。
