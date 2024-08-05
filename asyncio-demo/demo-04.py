#! -*-conding=: UTF-8 -*-
# 2023/4/19 13:47
import asyncio


async def nested():
    return 42


async def main():
    # Let's do it differently now and await it:
    print(await nested())  # will print "42".


if __name__ == '__main__':
    asyncio.run(main())
