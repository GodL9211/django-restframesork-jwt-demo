#! -*-conding=: UTF-8 -*-
# 2023/9/25 16:50
"""
    描述：python实现tree命令
"""

from pathlib import Path
import click
from typing import List

# ANSI颜色代码
BLUE = "\033[34m"
WHITE = "\033[0m"


def is_hidden(file: Path) -> bool:
    return file.name.startswith(".")


def get_entries(path: Path, show_hidden: bool = False) -> List[Path]:
    entries = list(path.iterdir())
    if not show_hidden:
        entries = [entry for entry in entries if not is_hidden(entry)]
    return sorted(entries, key=lambda entry: entry.is_file())


def print_tree(path: Path, symbol: str = "", max_depth: int = float("inf"), current_depth: int = 1,
               show_hidden: bool = False):
    if current_depth > max_depth:
        return

    entries = get_entries(path, show_hidden)
    total_entries = len(entries)
    num = 1
    for entry in entries:
        is_dir = entry.is_dir()
        entry_name = entry.name

        if num == total_entries:
            branch = "└─ "
            new_symbol = symbol + "     " if num == total_entries else symbol + "  │  "
        else:
            branch = "├─ "
            new_symbol = symbol + "  │  "

        if is_dir:
            click.echo(f"{symbol}{branch}{BLUE}{entry_name}{WHITE}")
            print_tree(entry, new_symbol, max_depth, current_depth + 1, show_hidden)
        else:
            click.echo(f"{symbol}{branch}{WHITE}{entry_name}")

        num += 1


@click.command()
@click.option("-p", "--path", default=".", type=click.Path(exists=True), help="要列出内容的目录路径")
@click.option("-d", "--depth", default=1, type=int, help="限制显示的深度")
@click.option("--hidden", is_flag=True, help="显示隐藏文件")
def main(path, depth, hidden):
    path = Path(path).resolve()
    click.echo(path)
    print_tree(path, max_depth=depth, show_hidden=hidden)


if __name__ == '__main__':
    main()
