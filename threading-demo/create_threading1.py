#! -*-conding=: UTF-8 -*-
# 2023/5/6 15:53
import time
from threading import Thread


def task():
    print("另外开始一个子线程做任务啦")
    time.sleep(1)  # 用time.sleep模拟任务耗时
    print("子线程任务结束啦")


if __name__ == '__main__':
    print("这里是主线程")
    # 创建线程对象
    t1 = Thread(target=task)
    # 启动
    t1.start()
    time.sleep(0.3)
    print("主线程依然可以干别的事")

