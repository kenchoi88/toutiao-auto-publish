#!/usr/bin/env bash
# 跨机共享记忆同步脚本
# 把 shared_memory/*.md 复制到本机 Claude memory/，并在 MEMORY.md 顶部插入醒目索引
# 幂等：重复跑安全，已存在的同名文件以仓库为准（覆盖）

set -e

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SHARED_DIR="$REPO_DIR/shared_memory"

# 检测本机 Claude memory 路径
# 支持 -d <dir> 参数显式指定目标 memory 目录
TARGET_DIR=""
if [ "$1" = "-d" ] && [ -n "$2" ]; then
    TARGET_DIR="$2"
fi

CWD_NORMALIZED=$(pwd | sed 's|/|-|g')
PROJECTS_DIR="$HOME/.claude/projects"

# 自动定位
if [ -z "$TARGET_DIR" ] && [ -d "$PROJECTS_DIR" ]; then
    # 1. 按当前cwd精确匹配
    for d in "$PROJECTS_DIR"/*; do
        [ -d "$d" ] || continue
        base=$(basename "$d")
        if [ "$base" = "$CWD_NORMALIZED" ] || [ "$base" = "${CWD_NORMALIZED#-}" ]; then
            TARGET_DIR="$d/memory"
            break
        fi
    done

    # 2. 找已有 memory/ 子目录的 project，按最近修改取第一个
    if [ -z "$TARGET_DIR" ]; then
        for d in $(ls -td "$PROJECTS_DIR"/*/ 2>/dev/null); do
            if [ -d "$d/memory" ]; then
                TARGET_DIR="$d/memory"
                echo "提示: 用 fallback 定位到已有 memory 目录: $TARGET_DIR"
                break
            fi
        done
    fi

    # 3. 都找不到：最近活跃的 project 下建一个 memory/
    if [ -z "$TARGET_DIR" ]; then
        d=$(ls -td "$PROJECTS_DIR"/*/ 2>/dev/null | head -1)
        if [ -n "$d" ]; then
            TARGET_DIR="${d%/}/memory"
            echo "提示: 在最近 project 下新建 memory: $TARGET_DIR"
        fi
    fi
fi

if [ -z "$TARGET_DIR" ]; then
    echo "错误: 找不到本机 Claude project 目录（~/.claude/projects/ 下任何子目录）"
    echo "请先用 Claude Code 至少跑一次会话，或用 -d <memory目录> 显式指定"
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
