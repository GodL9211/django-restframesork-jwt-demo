
"""
asyncio协程的执行时机
"""


import asyncio


async def main():
    print("Hello ...")
    await asyncio.sleep(1)
    print("... World!")


if __name__ == '__main__':
    a = main()
    print("还未执行")
    asyncio.run(a)  # 这里才会执行
