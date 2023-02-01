#! -*-conding=: UTF-8 -*-
# 2023/2/1 11:05
"""
https://docs.python.org/zh-cn/3/library/argparse.html#module-argparse
"""

import argparse

parser = argparse.ArgumentParser(description="test argparse", prog="Custom Projects")
# 位置参数，不齐时会报错退出
parser.add_argument("echo", help="echo the string you use here")  # 位置参数, 帮助文档
parser.add_argument("square", metavar="square", help="display a square of a given number", type=int,
                    choices=[1, 2, 3, 4, 5])  # 位置参数，默认类型为字符串，显示指定为int

parser.add_argument("-l", "--length", type=int, help="Length", default=10)

# 可选参数, 不传不会报错
parser.add_argument("--verbosity", help="increase output verbosity")
parser.add_argument("-v", "--verbose", help="increase output verbosity",
                    action="store_true")  # 不能赋值，仅作为标记，存在时为True, 否则为False

parser.add_argument("-V", "--Verbose", help="increase output verbosity",
                    action="count")

parser.add_argument('integers', metavar='N', type=int, nargs='+',  # nargs：该参数可用次数
                    help='an integer for the accumulator')
parser.add_argument('--sum', dest='accumulate', action='store_const',
                    const=sum, default=max,
                    help='sum the integers (default: find the max)')

args = parser.parse_args()
print(args.echo)
print(args.square ** 2)
print(args.length)

if args.verbosity:
    print("verbosity turned on")
print(args.Verbose)

print(args.accumulate(args.integers))

"""
lianhaifeng@D-LHF0307-01:/mnt/f/study/django-restframesork-jwt-demo/argparse-demo$ python3 01-prog.py hello 4
hello
16
"""

if __name__ == '__main__':
    pass
