#! -*-conding: UTF-8 -*-
# @公众号: 海哥python

"""
协程的应用： 检测域名是否可用
"""

import asyncio
import socket
from typing import Tuple
from keyword import kwlist

MAX_KEYWORD_LEN = 100


async def probe(domain: str) -> Tuple[str, bool]:
    loop = asyncio.get_running_loop()
    try:
        await loop.getaddrinfo(domain, None)
    except socket.gaierror:
        return domain, False
    return domain, True


async def main() -> None:
    names = (kw for kw in kwlist if len(kw) <= MAX_KEYWORD_LEN)
    domains = [f'{name}.com' for name in names]
    coros = [probe(domain) for domain in domains]
    for coro in asyncio.as_completed(coros):
        domain, is_valid = await coro
        mark = '*' if is_valid else '-'
        print(f'{mark} {domain}')


if __name__ == '__main__':
    asyncio.run(main())
