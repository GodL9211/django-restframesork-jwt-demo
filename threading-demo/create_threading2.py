#! -*-conding=: UTF-8 -*-
# 2023/5/6 15:53
import time
from threading import Thread


class NewThread(Thread):
    def __init__(self):
        Thread.__init__(self)  # 必须步骤

    def run(self):  # 入口是名字为run的方法
        print("开始新的线程做一个任务啦")
        time.sleep(1)  # 用time.sleep模拟任务耗时
        print("这个新线程中的任务结束啦")


if __name__ == '__main__':
    print("这里是主线程")
    # 创建线程对象
    t1 = NewThread()
    # 启动
    t1.start()
    time.sleep(0.3)  # 这里如果主线程结束，子线程会立刻退出，暂时先用sleep规避
    print("主线程依然可以干别的事")
