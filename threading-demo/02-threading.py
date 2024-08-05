#! -*-conding=: UTF-8 -*-
# 2023/2/1 19:29
"""
继承Thread类
"""
import time
from threading import Thread


class CountdownThread(Thread):
    def __init__(self, n):
        super().__init__()
        self.n = n

    def run(self):
        while self.n > 0:
            print('T-minus', self.n)
            self.n -= 1
            time.sleep(5)


def main():
    c = CountdownThread(5)
    c.start()


if __name__ == '__main__':
    main()
