---
name: 跨机共享记忆库使用规则
description: 5台机器agent共用的经验/教训分发机制，规则告诉每个agent如何使用和贡献
type: feedback
---

# 跨机共享记忆库

缺哥有5台机器各有常驻 agent（Air阿良 / neo小齐 / mini崔东山 / 台机崔巉 / neo2暂无人设）。各agent本机的记忆**物理隔离**，无法自动互通。为了避免"一个 agent 踩过的坑另一个 agent 再踩一次"，建立了这个跨机共享经验库。

位置：仓库 `~/code/头条自动发布/shared_memory/`

> ⚠️ 仓库虽叫"头条自动发布"，但 shared_memory 是**缺哥所有项目的跨机经验中枢**——头条/罐头/AI短剧/网站/米米学Python/任何调试经验……都该进。不要因为仓库名误以为只能放头条相关。

## 作为 agent，你需要做什么

### 1. 每次会话开始，先拉最新经验

```bash
cd ~/code/头条自动发布        # Mac
# cd /c/Users/kench/code/头条自动发布   # Windows Git Bash
git pull
bash shared_memory/sync_shared_memory.sh
```

这一步会把别的 agent 这段时间沉淀的经验同步到你本机的 memory/，让你能读到。sync 脚本是幂等的，重复跑安全。

### 2. 碰到值得跨机的教训/规则，主动写到 shared_memory

**Why:** 你本机 memory/ 只有你一个 agent 能看到。别的 agent 下次碰到同样问题还要重新解决一次，浪费缺哥的时间和 Claude 额度。

**How:**
```bash
# 直接把记忆文件写到仓库 shared_memory/，不要只写本机 memory/
vim ~/code/头条自动发布/shared_memory/feedback_xxx.md

# 或者更常见：某条本机记忆后来发现是跨机通用的，搬过去
cp ~/.claude/projects/<本机project>/memory/feedback_xxx.md \
   ~/code/头条自动发布/shared_memory/

cd ~/code/头条自动发布
git add shared_memory/feedback_xxx.md
git commit -m "shared: 加入 xxx 教训"
git push
```

## 什么值得跨机，什么不值得

**默认全跨**——按缺哥 2026-04-19 定的规矩："除了人设/人格，其他全加，没什么隐私，有的话我会单独强调"。

| ✓ 进 shared_memory | ✗ 不进（只留本机） |
|---|---|
| **任何项目的踩坑教训**：限流、网络、权限、API坑 | **人设/人格**：阿良/崔巉/崔东山/小齐/陈平安等 agent 自己的人物设定（`user_persona_*.md`） |
| **通用工作规则**：语言偏好、沟通方式、验证规则 | **缺哥单独标记"私密"** 的内容 |
| **基础事实**：仓库格局、SSH地址、脚本部署位置 | |
| **接口资源**：CDP端口、API接口、配置文件格式 | |
| **跨机操作流程**：分发、同步、定时任务 | |
| **任何项目状态/方向**：AI短剧、网站、罐头、数据导出、米米学Python等 | |
| **家庭/团队事实信息**：成员、设备阵容、订阅情况 | |

**判断秘诀**：写记忆默认进 shared_memory。除非是 agent 专属人设，或缺哥单独说"这事不要外传"。

不要因为"看着像私人"就排除——缺哥说了不怕，他若想私密会主动强调。

## 当前参与 agent

| 机器 | agent | SSH | 仓库路径 |
|------|-------|-----|---------|
| Air | 阿良（主力） | `ssh kenair@192.168.10.239` | `/Users/kenair/code/头条自动发布` |
| neo | 小齐 | `ssh kenchoios@192.168.10.243` | `/Users/kenchoios/code/头条自动发布` |
| mini | 崔东山 | `ssh kenchoimini@192.168.10.244` | `/Users/kenchoimini/code/头条自动发布` |
| 台机 | 崔巉（大师兄） | `ssh -p 2222 kench@192.168.10.8` | `C:/Users/kench/code/头条自动发布` |
| neo2 | （待定） | `ssh kenchoineo2@192.168.10.245` | `/Users/kenchoineo2/code/头条自动发布` |

## 同步时机

- **会话开始时**：干活前一定先 pull + sync，拿到最新教训
- **写完跨机记忆后**：立刻 commit + push，别拖
- **想到"这事其他agent是不是也会碰到"时**：想到就动，别等碰一堆再一起整理

## 给缺哥的承诺

这套机制落地后，缺哥不再需要反复提醒"那边agent不知道这事"——制度替代提醒，每个 agent 自己按流程走即可。
