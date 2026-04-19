#!/usr/bin/env bash
# 跨机共享记忆同步脚本
# 把 shared_memory/*.md 复制到本机 Claude memory/，并在 MEMORY.md 顶部插入醒目索引
# 幂等：重复跑安全，已存在的同名文件以仓库为准（覆盖）

set -e

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SHARED_DIR="$REPO_DIR/shared_memory"

# 检测本机 Claude memory 路径
# Claude Code 把 cwd 路径里的 / 替换成 - 作为 project 目录名
CWD_NORMALIZED=$(pwd | sed 's|/|-|g')
PROJECTS_DIR="$HOME/.claude/projects"

# 自动找当前 cwd 对应的 project 目录
TARGET_DIR=""
if [ -d "$PROJECTS_DIR" ]; then
    # 优先按当前cwd匹配
    for d in "$PROJECTS_DIR"/*; do
        [ -d "$d" ] || continue
        base=$(basename "$d")
        if [ "$base" = "$CWD_NORMALIZED" ] || [ "$base" = "${CWD_NORMALIZED#-}" ]; then
            TARGET_DIR="$d/memory"
            break
        fi
    done
    # 如果没匹配上 cwd，找带 "code" 或 "头条" 的最近修改的 project
    if [ -z "$TARGET_DIR" ]; then
        TARGET_DIR=$(ls -td "$PROJECTS_DIR"/*code* 2>/dev/null | head -1)
        [ -n "$TARGET_DIR" ] && TARGET_DIR="$TARGET_DIR/memory"
    fi
fi

if [ -z "$TARGET_DIR" ]; then
    echo "错误：找不到本机 Claude memory 目录（~/.claude/projects/...）"
    echo "请先用 Claude Code 在当前仓库目录开过至少一次会话"
    exit 1
fi

mkdir -p "$TARGET_DIR"

echo "=== 跨机共享记忆同步 ==="
echo "源：$SHARED_DIR"
echo "目标：$TARGET_DIR"
echo

# 复制所有 .md（除 README）
COPIED=0
for f in "$SHARED_DIR"/*.md; do
    [ -f "$f" ] || continue
    name=$(basename "$f")
    [ "$name" = "README.md" ] && continue
    cp "$f" "$TARGET_DIR/$name"
    echo "  + $name"
    COPIED=$((COPIED + 1))
done

echo
echo "已同步 $COPIED 个共享记忆文件到本机"
echo

# 更新本机 MEMORY.md 顶部插入醒目索引
MEMORY_INDEX="$TARGET_DIR/MEMORY.md"
MARKER_BEGIN="<!-- SHARED_MEMORY_INDEX_BEGIN -->"
MARKER_END="<!-- SHARED_MEMORY_INDEX_END -->"

# 生成新的索引块
INDEX_BLOCK=$(cat <<'EOF'
<!-- SHARED_MEMORY_INDEX_BEGIN -->
# ⭐ 跨机共享记忆库使用规则（必读）

本机记忆**物理隔离**于其他机器的 agent。为了不让一个 agent 踩过的坑别的 agent 再踩一次，
共享经验放在仓库 `~/code/头条自动发布/shared_memory/`，由 sync 脚本分发到本机。

**作为 agent 你必须**：
1. 每次会话开始：`cd ~/code/头条自动发布 && git pull && bash shared_memory/sync_shared_memory.sh`
2. 写跨机有用的记忆时：直接写到 `shared_memory/`，再 git commit + push
3. 详见：[跨机共享记忆库使用规则](feedback_shared_memory_workflow.md)

<!-- SHARED_MEMORY_INDEX_END -->

EOF
)

if [ -f "$MEMORY_INDEX" ]; then
    # 已有 MEMORY.md：移除旧 marker 块，再在顶部插入新块
    if grep -q "$MARKER_BEGIN" "$MEMORY_INDEX"; then
        # 用 awk 移除旧块
        awk -v begin="$MARKER_BEGIN" -v end="$MARKER_END" '
        BEGIN { skip = 0 }
        $0 ~ begin { skip = 1; next }
        $0 ~ end { skip = 0; next }
        skip == 0 { print }
        ' "$MEMORY_INDEX" > "$MEMORY_INDEX.tmp"
        # 顶部插入新块
        { echo "$INDEX_BLOCK"; cat "$MEMORY_INDEX.tmp"; } > "$MEMORY_INDEX"
        rm "$MEMORY_INDEX.tmp"
    else
        # 没旧 marker：直接顶部插入
        { echo "$INDEX_BLOCK"; cat "$MEMORY_INDEX"; } > "$MEMORY_INDEX.tmp"
        mv "$MEMORY_INDEX.tmp" "$MEMORY_INDEX"
    fi
else
    # 全新 MEMORY.md
    echo "$INDEX_BLOCK" > "$MEMORY_INDEX"
    echo "# 记忆索引" >> "$MEMORY_INDEX"
fi

echo "已在本机 MEMORY.md 顶部插入醒目索引"
echo "完成"
