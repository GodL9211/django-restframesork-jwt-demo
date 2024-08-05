#! -*-conding=: UTF-8 -*-
# 2023/2/1 19:29
"""
通过轮询退出线程，不推荐， 尤其是io阻塞操作场景， 比如，
如果一个线程一直阻塞在一个I/O操作上，它就永远无法返回，也就无法检查自己是否已经被结束了。要正确处理这些问题，你需要利用超时循环来小心操作线程。
通常是需要对阻塞时间设置超时。
"""
import time
from threading import Thread


class CountdownTask:
    def __init__(self):
        self._running = True

    def terminate(self):
        self._running = False

    def run(self, n):
        while self._running and n > 0:
            print('T-minus', n)
            n -= 1
            time.sleep(5)


def main():
    c = CountdownTask()
    t = Thread(target=c.run, args=(10,))
    t.start()
    c.terminate()  # Signal termination
    t.join()  # Wait for actual termination (if needed)


if __name__ == '__main__':
    main()
