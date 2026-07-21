#!/usr/bin/env bash
# 上传本脚本到任意课程服务器后，在服务器上运行。
# 它会从 GitHub 稀疏克隆/更新所选讲次，不需要本机到服务器的 rsync 或服务器映射表。
# 兼容 macOS/Linux 常见 Bash；服务器需要 Git 2.25+。

set -euo pipefail

REPO_URL="https://github.com/Jafekin/advanced_python_course.git"
BRANCH="main"
OUTPUT_DIR="/workspace"
CACHE_DIR="${HOME}/.cache/advanced_python_course"
SELECTION=""
LIST_ONLY=0

LESSONS=(
    "第1讲"
    "第2讲"
    "第3讲"
    "第4讲"
    "第5讲"
    "第6讲"
    "第7讲"
    "第8讲"
)

usage() {
    cat <<'EOF'
用法（在服务器上运行）：
  bash pull_lesson_from_github.sh [选项]

脚本首次运行会从 GitHub 创建稀疏克隆；之后只更新所选讲次，
并执行 git pull --ff-only origin main。没有指定讲次时会要求输入数字 1–8。

选项：
  -l, --lesson NUM        选择讲次，NUM 必须是 1–8
  -d, --dir PATH          讲次文件输出目录（默认：/workspace）
      --cache-dir PATH     Git 缓存目录（默认：$HOME/.cache/advanced_python_course）
  -b, --branch BRANCH     GitHub 分支（默认：main）
  -r, --repo URL          Git 仓库地址（默认：Jafekin/advanced_python_course）
      --list              列出可选讲次后退出
  -h, --help              显示帮助

示例：
  bash pull_lesson_from_github.sh
  bash pull_lesson_from_github.sh --lesson 6
  bash pull_lesson_from_github.sh --lesson 3 --dir /srv/course
EOF
}

die() {
    printf '错误：%s\n' "$*" >&2
    exit 1
}

require_command() {
    command -v "$1" >/dev/null 2>&1 || die "未找到命令：$1"
}

while [ "$#" -gt 0 ]; do
    case "$1" in
        -l|--lesson)
            [ "$#" -ge 2 ] || die "$1 需要讲次名称或编号"
            SELECTION="$2"
            shift 2
            ;;
        -d|--dir)
            [ "$#" -ge 2 ] || die "$1 需要目录路径"
            OUTPUT_DIR="$2"
            shift 2
            ;;
        --cache-dir)
            [ "$#" -ge 2 ] || die "$1 需要目录路径"
            CACHE_DIR="$2"
            shift 2
            ;;
        -b|--branch)
            [ "$#" -ge 2 ] || die "$1 需要分支名"
            BRANCH="$2"
            shift 2
            ;;
        -r|--repo)
            [ "$#" -ge 2 ] || die "$1 需要 Git 仓库 URL"
            REPO_URL="$2"
            shift 2
            ;;
        --list)
            LIST_ONLY=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        *)
            die "未知选项：$1（使用 --help 查看帮助）"
            ;;
    esac
done

print_lessons() {
    local i
    printf '可选讲次：\n'
    for ((i = 0; i < ${#LESSONS[@]}; i++)); do
        printf '  %s) %s\n' "$((i + 1))" "${LESSONS[$i]}"
    done
}

if [ "$LIST_ONLY" -eq 1 ]; then
    print_lessons
    exit 0
fi

if [ -z "$SELECTION" ]; then
    print_lessons
    printf '请选择要从 GitHub 更新的讲次（请输入数字 1-8，q 退出）： '
    IFS= read -r SELECTION
    [ "$SELECTION" = "q" ] || [ "$SELECTION" = "Q" ] && exit 0
fi

[[ "$SELECTION" =~ ^[1-8]$ ]] || die "请输入数字 1-8（收到：$SELECTION）"
index=$((SELECTION - 1))
LESSON="${LESSONS[$index]}"

require_command git

# --sparse / sparse-checkout 需要 Git 2.25+；在非 Git 目录执行 `git sparse-checkout -h` 会失败，
# 因而这里检查版本号，而不是调用该子命令。
git_version="$(git --version | awk '{print $3}')"
git_major="${git_version%%.*}"
git_version_rest="${git_version#*.}"
git_minor="${git_version_rest%%.*}"
case "$git_major:$git_minor" in
    *[!0-9:]*|:) die "无法识别 Git 版本：$git_version" ;;
esac
if [ "$git_major" -lt 2 ] || { [ "$git_major" -eq 2 ] && [ "$git_minor" -lt 25 ]; }; then
    die "服务器 Git 版本为 $git_version；稀疏检出需要 Git 2.25 或更高版本。"
fi

# Git 缓存与课程输出必须分离：CloudStudio 等环境的 /workspace 往往已是别的仓库，
# 不能改它的 origin。缓存放在用户目录，/workspace 只得到目标讲次的普通文件。
if [ -e "$CACHE_DIR" ] && [ ! -d "$CACHE_DIR/.git" ]; then
    die "Git 缓存目录已存在但不是仓库：$CACHE_DIR。请处理该目录，或使用 --cache-dir 指定其他位置。"
fi

if [ ! -d "$CACHE_DIR/.git" ]; then
    printf '首次下载：从 %s 的 %s 创建讲次缓存……\n' "$REPO_URL" "$BRANCH"
    mkdir -p "$(dirname "$CACHE_DIR")"
    git clone --depth 1 --filter=blob:none --sparse --branch "$BRANCH" "$REPO_URL" "$CACHE_DIR"
else
    current_origin="$(git -C "$CACHE_DIR" remote get-url origin 2>/dev/null || true)"
    [ -n "$current_origin" ] || die "Git 缓存没有配置 origin：$CACHE_DIR"
    if [ "$current_origin" != "$REPO_URL" ]; then
        die "Git 缓存的 origin 与目标不一致：$current_origin。请使用 --cache-dir 指定新缓存目录。"
    fi
fi

# 非 cone 模式显式只匹配该讲次的全部文件；缓存中也不检出 assets、scripts、README 等根目录内容。
git -C "$CACHE_DIR" sparse-checkout set --no-cone "$LESSON/**"
git -C "$CACHE_DIR" checkout "$BRANCH"
printf '拉取 GitHub 最新内容：%s / %s……\n' "$BRANCH" "$LESSON"
git -C "$CACHE_DIR" pull --ff-only origin "$BRANCH"

# 仅同步选中讲次到输出目录。许多 CloudStudio 容器没有 rsync，故使用系统通常自带的 tar。
# 先在同一输出目录创建完整暂存副本，再替换旧的第X讲目录，避免留下已从 GitHub 删除的旧文件。
require_command tar
output_parent="${OUTPUT_DIR%/}"
target_dir="$output_parent/$LESSON"
staging_dir="$output_parent/.${LESSON}.staging.$$"
backup_dir=""
mkdir -p "$output_parent"
[ ! -e "$staging_dir" ] || die "暂存目录已存在：$staging_dir"
mkdir -p "$staging_dir"
cleanup_staging() { rm -rf "$staging_dir"; }
trap cleanup_staging EXIT HUP INT TERM
printf '同步讲次文件到：%s\n' "$target_dir"
tar -C "$CACHE_DIR/$LESSON" -cf - . | tar -C "$staging_dir" -xf -

# 新内容已完整写入暂存目录后，才移动旧目录；若替换失败会尽力恢复旧目录。
if [ -e "$target_dir" ]; then
    backup_dir="$output_parent/.${LESSON}.backup.$$"
    [ ! -e "$backup_dir" ] || die "备份目录已存在：$backup_dir"
    mv "$target_dir" "$backup_dir"
fi
if ! mv "$staging_dir" "$target_dir"; then
    [ -z "$backup_dir" ] || mv "$backup_dir" "$target_dir"
    die "无法替换讲次目录：$target_dir"
fi
trap - EXIT HUP INT TERM
[ -z "$backup_dir" ] || rm -rf "$backup_dir"

printf '\n完成：%s 已更新到 %s\n' "$LESSON" "${OUTPUT_DIR%/}/$LESSON"
printf '当前稀疏检出目录：\n'
git -C "$CACHE_DIR" sparse-checkout list
