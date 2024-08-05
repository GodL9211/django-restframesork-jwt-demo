#! -*-conding=: UTF-8 -*-
# 2023/9/25 16:50
"""
    描述：python实现tree命令
"""

from pathlib import Path
from typing import List

# 黑名单 不想列出的目录
blacklist: List[str] = [".git", ".idea"]
# 指定列出哪个目录下的所有内容，使用当前路径的上一层路径
rpath: Path = Path(__file__).resolve().parent


def dir_and_file(path: Path, symbol: str = ""):
    # 列出所有目录和文件 同时统计数量用于判断
    file_list = [entry for entry in path.iterdir() if entry.name not in blacklist]
    total_num = len(file_list)
    num = 1
    for entry in file_list:
        # 路径合并 递归调用时继续向下传递
        if entry.is_file():
            # 判断是否为最后一个
            prefix = "  └─ " if num == total_num else "  ├─ "
            print(f"{symbol}{prefix}{entry.name}")
        else:
            # 判断目录是否为最后一个 如果是则使用不同的符号
            prefix = "  └─ " if num == total_num else "  ├─ "
            print(f"{symbol}{prefix}{entry.name}")
            dir_and_file(entry, f"{symbol}{'     ' if num == total_num else '  │  '}")
        num += 1


if __name__ == '__main__':
    print(rpath)
    dir_and_file(rpath)
