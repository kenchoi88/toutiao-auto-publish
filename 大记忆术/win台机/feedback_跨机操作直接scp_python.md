---
name: 跨机操作直接 scp + Python 脚本,不要 ssh 直接命令
description: PowerShell + ssh + zsh 三层嵌套引号转义经常踩 zsh nomatch / glob expand / pipe 当命令错,跨机批操作直接 scp + python3 脚本一气呵成
type: feedback
originSessionId: 65e7943b-4b50-4d8f-8d15-a85ca3997cff
---
**踩过的坑 (2026-05-11)**: 5 机清 .bak 文件,我先后试了:
1. `ssh user@ip "find ... -name '*.bak'"` — zsh nomatch silently fail (空输出)
2. `ssh ... "find ... \( -name '*' \)"` — 转义层级把 `(` 吃掉
3. `ssh ... 'ls | grep -E "a|b" | xargs rm'` — zsh 把 `a|b` 中的 `|` 当 pipe,把 `b` 当命令
4. `ssh ... 'bash -c "find ..."'` — bash 包装也没救,引号还是被 PowerShell 剥

**根因**: PowerShell 单引号字符串里的双引号是字面量,但 ssh 把整个字符串作为单参数传给 zsh 后,zsh 重新解析,quotes 状态不可预测。zsh 严格模式 nomatch 默认报错,glob/pipe/通配符全部踩雷。

**铁律**: **跨机批操作 = 写 .py 脚本 + scp + python3 跑 + rm**,不要试图把 shell 命令塞进 ssh 引号里。

```powershell
# ❌ 错: 试图 ssh 直接命令
ssh user@ip "find ... -name '*.bak' -delete"

# ✅ 对: scp Python 脚本
scp local.py user@ip:~/script.py
ssh user@ip 'python3 ~/script.py && rm ~/script.py'
```

写 .py 用 `os.path.expanduser('~')` + `glob.glob()` 处理路径,不会有引号转义问题,中文目录名 + UTF-8 编码正常。

---

**例外:单参数 ssh inline 测连通/取一个值** — 不写 .py,但**必须用单引号**让远端 bash 展开,不要双引号被 PowerShell 抢先展开:

```powershell
# ❌ 错(2026-05-13 测 TS 时踩):双引号 PowerShell 本地展开 $(...),Get-Date 不认 `+%H:%M:%S` 报错,远端啥都没收到
ssh user@ip "echo $(hostname) $(date +%H:%M:%S)"

# ✅ 对:单引号字面量,ssh 把字符串原样塞远端 bash,$( ) 在远端展开
ssh user@ip 'echo $(hostname) $(date +%H:%M:%S)'
```

**判别**:命令里凡含 `$()` `$VAR` `\`...\`` 这类 shell 展开,inline ssh 一律用**单引号**。复杂的还是按上面铁律走 .py。

**为何重要**: 调 4 次 ssh + 转义 + 重传 + 验证 ≈ 写 1 个 .py + scp + 跑(更快 + 更稳)。V1102.6/V1102.7 推送一直用这个模式,清 .bak 时偷懒试一行命令,结果 4 次失败 + 缺哥怒。
