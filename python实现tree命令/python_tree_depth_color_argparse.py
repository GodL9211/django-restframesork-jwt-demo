#! -*-conding=: UTF-8 -*-
# 2023/9/25 16:50
"""
    描述：python实现tree命令
"""

from pathlib import Path
import argparse

from typing import Optional

# 黑名单 不想列出的目录
blacklist = [".git", ".idea"]

# ANSI颜色代码
BLUE = "\033[34m"
WHITE = "\033[0m"


def is_hidden(file: Path) -> bool:
    return file.name.startswith(".")


def get_entries(path: Path, show_hidden: bool = False):
    entries = list(path.iterdir())
    if not show_hidden:
        entries = [entry for entry in entries if not is_hidden(entry)]
    return sorted(entries, key=lambda entry: entry.is_file())


def print_tree(path: Path, depth: Optional[int], show_hidden: bool = False, indent: str = "", is_last: bool = True):
    entries = get_entries(path, show_hidden)
    total_entries = len(entries)
    for i, entry in enumerate(entries):
        is_dir = entry.is_dir()
        entry_name = entry.name

        if i == total_entries - 1:
            branch = "└─ "
            new_indent = indent + "    " if is_last else indent + "│   "
        else:
            branch = "├─ "
            new_indent = indent + "│   "

        if is_dir:
            print(f"{indent}{branch}{BLUE}{entry_name}{WHITE}")
            if depth is None or (depth and depth > 1):
                print_tree(entry, None if depth is None else depth - 1, show_hidden, new_indent, i == total_entries - 1)
        else:
            print(f"{indent}{branch}{entry_name}")


def main():
    parser = argparse.ArgumentParser(description="Python实现tree命令")
    parser.add_argument("-p", "--path", type=str, nargs="?", default=".", help="要遍历的目录路径")
    parser.add_argument("-d", "--depth", type=int, default=1, help="限制显示的层数")
    parser.add_argument("--hidden", action="store_true", help="显示隐藏文件")
    args = parser.parse_args()
    path = Path(args.path).resolve()
    print(path)
    print_tree(path, args.depth, args.hidden)


if __name__ == "__main__":
    main()
