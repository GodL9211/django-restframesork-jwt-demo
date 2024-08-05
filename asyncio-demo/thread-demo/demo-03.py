#! -*-conding=: UTF-8 -*-
# 2023/4/20 10:51


import time
import threading

# 创建事件对象
event = threading.Event()


def dis_class():
    time.sleep(5)
    event.wait()
    print('同学们下课了')


def bell():
    time.sleep(3)
    print('下课铃声响了')
    event.set()


if __name__ == '__main__':
    t1 = threading.Thread(target=bell)
    t2 = threading.Thread(target=dis_class)
    t1.start()
    t2.start()
    t1.join()
    t2.join()

if __name__ == '__main__':
    pass
