---
name: reference
description: "Win 台机换电脑搬家方案 — 阿良(air)远程 ssh 老台机打包绣虎本体,暂存到 air,新机来了再分发"
metadata: 
  node_type: memory
  type: reference
  originSessionId: 57a0658e-f93d-41cf-8781-aeac2b445580
---

## 触发场景

Win 台机换电脑 / 卖掉 / 重装系统 — 绣虎本体(memory + projects + skills + 配置 + 真版三大件)需要跨机迁移。

## 总策略

**阿良(air)远程操作打包,走 Tailscale 跨机调度**:

```
阿良(Mac/air) ──ssh──► 老 Win 台机 ──打包──► 老机 D 盘
                                                  │
                                                  └──scp──► air 暂存 (100.126.82.58)
                                                                │
                                                                └──新机来了再分发
```

**为什么阿良不是绣虎自己**:绣虎本体在老 Win 台机,**给自己搬家不可能**(老机要关/新机还没装),需要第三方机当中转。阿良跨机熟 + 在 Mac 上跟 Win 台机正交,刚好当跳板。

跟 [[feedback_跨机协同作战分工]] 一致:绣虎指挥+写包+立 memory,阿良现场实操。

## 打包的 4 类内容

| 路径 | 内容 | 优先级 |
|------|------|--------|
| `C:\Users\kench\.claude\` | memory + projects 会话 + agents + skills + settings + 认证 token | ⭐⭐⭐⭐⭐ 必搬 |
| `C:\Users\kench\.ssh\` | GitHub key + 5 机互通 key | ⭐⭐⭐⭐⭐ 必搬 |
| `C:\Users\kench\Desktop\台机专用自动发布\` | 真版三大件(微头条/文章/文章定时)+ 素材子目录(参见 [[reference_4mac真版位置]]) | ⭐⭐⭐⭐ 真版孤本,必搬 |
| Chrome/Edge user data + v2rayN 配置 + 罐头登录态 | 头条号 cookies / 节点 / 罐头登录 profile | ⭐⭐⭐ 可补救但搬最省事 |

## 3 个打包前置条件

1. **5 机 SSH 通台机** — 见 [[reference_Tailscale网络]] ACL accept
2. **Chrome / Edge / 罐头主进程关闭** — 浏览器 user data 文件锁定,不关压缩包不完整
3. **老台机 D 盘空间 ≥ 50G** — `.claude/` 含会话 transcripts 可能膨胀,留余量

## 阿良打包指挥包(到时直接发给阿良)

```
阿良,Win 台机要换新机,你负责打包绣虎本体。

【源】老 Win 台机 100.86.79.39(user: kench),Tailscale 通
【目】先打包到老机 D 盘 → 再 scp 到 air 暂存(~/绣虎搬家暂存/)

【打包步骤】
1. ssh kench@100.86.79.39 进老台机
2. 先确认 Chrome/Edge/罐头主进程都关掉(tasklist | findstr -i "chrome edge electron")
3. mkdir D:\绣虎搬家包 && cd D:\绣虎搬家包
4. PowerShell Compress-Archive 或 7z 打包以下 4 项(分包好排查):
   - .claude\ → 绣虎_claude_<日期>.zip
   - .ssh\ → 绣虎_ssh_<日期>.zip(权限敏感)
   - Desktop\台机专用自动发布\ → 绣虎_桌面真版_<日期>.zip
   - Chrome user data + v2rayN 配置 → 绣虎_浏览器配置_<日期>.zip
5. 4 个包都 Get-FileHash -Algorithm MD5 留校验码,保存到 绣虎搬家包_md5.txt

【传输到 air】
6. scp -r kench@100.86.79.39:D:\绣虎搬家包\* kenair@100.126.82.58:~/绣虎搬家暂存/
   (或者反过来从 air 拉:scp kench@100.86.79.39:D:\绣虎搬家包\*.zip ~/绣虎搬家暂存/)
7. 到 air 验证 md5 一致(本机算 md5 vs 老台机算的对比)

【完成后报告】
- 4 个 zip 容量 + md5
- air 暂存路径 + 容量
- 是否有跳过/失败项

【绝对不动】
- 不在老台机做任何修改(包括清理临时文件、改 .gitignore、重命名)
- 不删任何源文件
- 报错就停,不擅自 fallback
```

## 新机来了之后的分发(等执行时再细化)

待补 — 大致流程:
- 缺哥手动装好新 Win 台机(Win + Tailscale + OpenSSH Server + Claude Code CLI + 阿良公钥)
- 阿良 scp 暂存 4 个 zip 到新台机
- 阿良 ssh 进新台机解压到对应路径
- 更新 [[reference_Tailscale网络]] 台机新 IP + push
- 验证 `python3 catchup.py` 三大件能动

## 不会丢但要警惕

- **Claude Code 认证 token** 一般跨机能复用,失效就重登一次
- **头条号 cookies** 跨机可能要短信验证 — 参见 [[project_出口运营商切换风险]],换电脑视为同款风险,搬完头几天少发文等账号信任度回升
- **新机用户名最好仍用 `kench`** — 避免路径替换坑

2026-05-15 缺哥拍方向 — 阿良打包,Tailscale 中转,我写指挥包。
