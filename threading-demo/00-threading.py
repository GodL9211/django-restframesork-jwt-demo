#! -*-conding=: UTF-8 -*-
# 2023/2/1 19:20
"""
简单起个线程
"""

import time
from threading import Thread


def countdown(n):
    while n > 0:
        print("T-minus\n", n)
        n -= 1
        time.sleep(5)


def main():
    t = Thread(target=countdown, args=(10,))
    t.start()
    # t.join()  # t线程结束才会往下执行

    if t.is_alive():
        print("Still running")
    else:
        print("Complete")
    t.join()


if __name__ == '__main__':
    main()
