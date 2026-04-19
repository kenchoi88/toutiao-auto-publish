# 跨机共享记忆库（缺哥所有项目）

5台机器（Air/neo/mini/台机/neo2）的 Claude/agent 共用的经验/教训/规则记忆。

> ⚠️ 注意：仓库虽叫"头条自动发布"，但 `shared_memory/` 是**缺哥所有项目的跨机经验中枢**——不限于头条/罐头业务。AI短剧、网站计划、米米学Python、调试任意脚本……任何在某台机沉淀下来的经验，都该进这里让其他agent立刻用得上。

避免每台机的 agent 接手干活时再走一次别的 agent 已经踩过的坑。

## 同步流程

```bash
# 任意机器拉到最新仓库后，跑一次：
cd /Users/<your-user>/code/头条自动发布   # Mac
# 或 cd C:/Users/kench/code/头条自动发布     # Windows
bash shared_memory/sync_shared_memory.sh
```

脚本会把 `shared_memory/*.md` 复制到本机 Claude 记忆目录，并把索引追加到本机 `MEMORY.md`。已存在的同名文件会覆盖（共享记忆以仓库为准）。

## 什么进 shared_memory，什么不进

**默认全进**——按缺哥 2026-04-19 定的规矩："除了人设/人格，其他全加，没什么隐私，有的话我会单独强调"。

| ✓ 进 | ✗ 不进 |
|---|---|
| **任何项目的踩坑教训**：限流、网络、权限、API坑 | **人设/人格**：阿良/崔巉/崔东山/小齐/陈平安各自的人物设定（`user_persona_*.md`） |
| **工作规则**：通用语言/沟通/验证规则 | 缺哥**单独标记**为"私密"的内容 |
| **基础信息**：仓库格局、SSH连接、脚本部署位置 | |
| **接口资源**：CDP端口、API接口、配置格式 | |
| **跨机操作流程**：分发、同步、定时任务 | |
| **任何项目的状态/方向**：AI短剧、网站、罐头、数据导出等 | |
| **家庭/团队事实信息**：米米学Python、儿子学习状态、AI助手阵容 | |

## 写新记忆时的判断

写一条记忆，**默认进 shared_memory**。除非：
1. 内容是某个 agent 专属人设（写进 `user_persona_*.md`，留本机）
2. 缺哥单独强调"这事不要外传"

需要时直接：
```bash
# 直接写在 shared_memory/
vim ~/code/头条自动发布/shared_memory/xxx.md
# 或本机记忆里写完后顺手 cp 一份过来
cp ~/.claude/projects/<本机project>/memory/xxx.md ~/code/头条自动发布/shared_memory/

cd ~/code/头条自动发布 && git add shared_memory/xxx.md && \
  git commit -m "shared: xxx" && git push
```

## 文件命名约定

跟本机记忆库一致：`feedback_*.md` `project_*.md` `reference_*.md` `user_*.md`

每个文件保持完整的 frontmatter（name/description/type）。

## 重要原则

shared_memory 同步是**单向**的（仓库→本机覆盖）。本机改了同名文件**不会**反向推回仓库——agent 必须主动 cp + commit + push 才能让别人看到。
