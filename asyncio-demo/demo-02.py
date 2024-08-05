#! -*-conding=: UTF-8 -*-
# 2023/4/19 11:50

"""
跟同步执行花费一样的时间？为什么呢？
"""


# 导入异步编程库asyncio和时间操作库time
import asyncio
import time


# 定义一个异步函数，用于延迟一段时间后打印信息
# 参数delay: 延迟的时间，单位为秒
# 参数what: 延迟后要打印的信息
async def say_after(delay, what):
    # 模拟异步操作，睡眠指定的延迟时间
    await asyncio.sleep(delay)
    # 打印信息
    print(what)


# 定义主异步函数，用于演示say_after函数的使用
async def main():
    # 打印开始时间
    print(f"started at {time.strftime('%X')}")
    # 调用say_after函数，并等待"hello"信息的打印
    await say_after(1, "hello")
    # 调用say_after函数，并等待"world"信息的打印
    await say_after(2, "world")
    # 打印结束时间
    print(f"finished at {time.strftime('%X')}")


# 程序入口点
if __name__ == '__main__':
    # 运行主异步函数
    asyncio.run(main())
