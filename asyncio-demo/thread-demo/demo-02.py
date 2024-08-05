#! -*-conding=: UTF-8 -*-
# 2023/4/20 10:36

import threading


class Factory(threading.Thread):

    def __init__(self, cond):
        super(Factory, self).__init__(name="口罩生产厂家")
        self.cond = cond

    def run(self):
        with self.cond:
            self.cond.wait()
            print("{}:生产了10万个口罩，快来拿".format(self.name))
            self.cond.notify()

            self.cond.wait()
            print("{}:又生产了100万个口罩发往武汉".format(self.name))
            self.cond.notify()

            self.cond.wait()
            print("{}:加油，武汉！".format(self.name))
            self.cond.notify()


class wuhan(threading.Thread):
    def __init__(self, cond):
        super(wuhan, self).__init__(name="武汉志愿者")
        self.cond = cond

    def run(self):
        with self.cond:
            print("{}:能帮我们生产一批口罩吗？".format(self.name))
            self.cond.notify()
            self.cond.wait()

            print("{}:谢谢你们".format(self.name))
            self.cond.notify()
            self.cond.wait()

            print("{}:一起加油".format(self.name))
            self.cond.notify()
            self.cond.wait()


if __name__ == "__main__":
    lock = threading.Condition()
    factory = Factory(lock)
    wuhan = wuhan(lock)
    factory.start()
    wuhan.start()
