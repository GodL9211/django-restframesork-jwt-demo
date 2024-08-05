#! -*-conding=: UTF-8 -*-
# 2023/5/6 16:06


import time
from threading import Thread


def task1():
    print("开始子线程1做任务1啦")
    time.sleep(1)  # 用time.sleep模拟任务耗时
    print("子线程1中的任务1结束啦")


def task2():
    print("开始子线程2做任务2啦")
    for i in range(5):
        print("任务2-{}".format(i))
        time.sleep(1)
    print("子线程2中的任务2结束啦")


if __name__ == '__main__':
    print("这里是主线程")
    # 创建线程对象
    t1 = Thread(target=task1)
    t2 = Thread(target=task2)
    t2.setDaemon(True)  # 设置为守护进程，必须在start之前
    # 启动
    t1.start()
    t2.start()
    time.sleep(1)
    print("主线程结束了")
