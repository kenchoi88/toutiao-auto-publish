---
name: 桌面是真,仓库是镜像 —— Win 台机配置同步方向死规则
description: Win 台机三大件实际运行在 ~/Desktop/台机专用自动发布/,git 仓库 win台机/ 是备份镜像;改动从桌面起,push 是反向同步
type: feedback
originSessionId: ed3bc523-a7f0-4efd-9774-5194c563ed34
---
**红线:** Win 台机的脚本 + 配置实际跑在 `~/Desktop/台机专用自动发布/GTG_青春小馆*/`,**git 仓库 `win台机/GTG_青春小馆*/` 是备份镜像,不是运行版**。任何改动:

1. **先改桌面**(真实运行版),验证生效
2. **再 cp 到仓库 + commit + push**(同步备份)

不能反过来「改仓库 → push 完事」,那样桌面跑的还是旧版,我下午就这么干了,被骂三轮。

**Why:** 2026-04-26 下午我做"三套脚本死磕重构 + 配置加待补漏 sheet",全部改在仓库,push 走人。结果:
- 桌面跑的还是 4-26 凌晨旧版,新功能一个没跑上
- 桌面 xlsx 字段跟新代码对不齐(列名错 / 缺 sheet)
- 缺哥晚上发文「跟屎一样」全因这个分裂

**How to apply:**

**改 Win 台机三大件 .py 时(一气呵成,不停下来问 push 不 push):**
1. 改 `~/Desktop/台机专用自动发布/GTG_青春小馆*/[gtg_batch.py | gtg_timer.py]`
2. **跑一次验证**(go.bat 启动看日志能不能起)
3. cp 到 `win台机/GTG_青春小馆*/` 仓库镜像
4. git add + commit + **push 到 GitHub**(同步 = push,不是 commit 本地)
5. **绝不**说"已存到本地仓库"这种废话——本地仓库只是中转,**目的地是 GitHub**

**改 Win 台机三大件 xlsx(配置 + 账号)时:**
1. 改桌面 xlsx
2. cp 到仓库镜像(.gitignore 已配例外允许 4 个 xlsx 入仓)
3. git add + commit + push

**绝对不要:**
- ❌ 只改仓库版不改桌面 → 等于没改
- ❌ 改 xlsx 时凭印象加 sheet/列名 → 必须先看实际跑的代码用什么列名
- ❌ 自作主张同步「永久跳过」之类的用户数据 → 见 [project_账号配置sheet_权属.md](project_账号配置sheet_权属.md)

**.gitignore 例外清单(2026-04-27 配置):**
```
*.xlsx
!win台机/GTG_青春小馆定时自动发布/账号配置.xlsx
!win台机/GTG_青春小馆定时自动发布/定时配置.xlsx
!win台机/GTG_青春小馆自动发布微头条/账号配置.xlsx
!win台机/GTG_青春小馆自动发布文章/账号配置.xlsx
```

## Mac 各机情况(2026-04-28 实测纠正)

**Mac 上"桌面"可能是真目录,也可能是 symlink → ~/code/**,改前必须 `ls -la $HOME/Desktop/Mac*` 看是不是箭头(`l` 开头 = symlink):

| 机器 | 大件 | 桌面性质 | 真版位置 |
|---|---|---|---|
| mini | 微头条自动发布 | 真目录 | `/Users/kenchoimini/Desktop/微头条自动发布/`(2026-04-28 已去 Mac 前缀) |
| mini | 文章自动发布 | 真目录 | `/Users/kenchoimini/Desktop/文章自动发布/`(2026-04-28 已去 Mac 前缀) |
| mini | **文章定时自动发布** | **symlink** | 真版 `/Users/kenchoimini/code/头条自动发布/Mac文章定时自动发布/`(待与代码同步重命名) |

(其它机 air/neo2 同样要逐一实测,别假设。)

**改 mini 文章定时:** 改 ~/code/ 那个真目录,桌面 symlink 自动跟。**改名要同时改 .command 硬编路径**(.command 引用 `$HOME/Desktop/Mac文章定时自动发布`)。

**判定规则:**
- `ls -la X` 出现 `lrwxr-xr-x ... -> /path/to/真版` → 桌面是 symlink
- 否则 → 桌面是真目录
- ps + lsof | grep cwd 看进程实际跑的目录,以这个为最终真相

**mini 特殊:iCloud 云盘接管桌面**(2026-04-28 缺哥确认)
- mini 的 `~/Desktop/` 实际是 **iCloud Drive 的 Desktop 同步文件夹**(macOS Desktop & Documents in iCloud)
- 因此 Finder 侧边栏没"桌面"项 — 桌面在 iCloud Drive 下访问
- 跨机操作引用 mini 文件时,**永远用绝对路径** `/Users/kenchoimini/Desktop/...` — 不要用 `~/`(本机和其它机展开不同)
- 描述位置显式带完整路径,不要只说"桌面"

**iCloud Desktop 副作用警惕:**
- docx 可能"未下载"状态(显示云图标),首次访问会触发下载延迟
- 跨设备会同步 — 其它登 kenchoi315@gmail.com Apple ID 的设备也能看到这些文件
- iCloud 抖动可能让脚本读不到文件 / 移文件失败 → 需要 `brctl download` 之类强制 pull(待验)
