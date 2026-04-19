# 跨机共享记忆库

5台机器（Air/neo/mini/台机/neo2）的 Claude/agent 共用的"经验/教训/规则"记忆。

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

| ✓ 进 | ✗ 不进 |
|---|---|
| **踩坑教训**：限流根因、网络坑、权限坑 | **人设**：阿良/崔巉/崔东山/小齐/陈平安人设 |
| **工作规则**：通用语言/沟通/验证规则 | **强人格偏好**：每台机agent定位独有的 |
| **基础信息**：仓库格局、SSH连接、脚本部署位置 | **家庭隐私**：米米、儿子、深夜长谈 |
| **接口资源**：CDP端口、API接口、配置格式 | **特定项目**：AI短剧、网站计划等私人项目 |
| **跨机操作流程**：分发、同步、定时任务 | **单机配置**：本机特有的隐藏应用、本地路径 |

## 写新记忆时的判断

每写一条记忆，先问一句"如果换一台机的agent接手这件事，他需要这条吗"——
- 需要 → 直接写进 `shared_memory/`，下次sync传到4台
- 不需要 → 只写本机 `~/.claude/projects/.../memory/`

涉及人设、家庭隐私、单机偏好的，**永远不进 shared_memory**。

## 文件命名约定

跟本机记忆库一致：`feedback_*.md` `project_*.md` `reference_*.md`

每个文件保持完整的 frontmatter（name/description/type）。
