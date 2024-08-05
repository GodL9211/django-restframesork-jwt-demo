#! -*-conding=: UTF-8 -*-
# 2023/4/20 10:05
import threading
import time


loops = [4, 2]


def loop(nloop, nsec):
    print(f"start loop {nloop} at {time.ctime()}")
    time.sleep(nsec)
    print(f"end loop {nloop} at {time.ctime()}")


def main():
    print(f"start main at {time.ctime()}")
    threads = []
    nloops = range(len(loops))
    for i in nloops:
        t = threading.Thread(target=loop, args=(i, loops[i]))
        threads.append(t)

    for i in nloops:
        threads[i].start()

    for i in nloops:
        threads[i].join()
    print(f"end main at {time.ctime()}")


if __name__ == '__main__':
    main()
