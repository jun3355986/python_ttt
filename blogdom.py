import asyncio
import socket
from keyword import kwlist

MAX_KEYWORD_LEN = 4

async def probe(domain: str) -> tuple[str, bool]:
    # 获取当前事件循环
    loop = asyncio.get_running_loop()
    try:
        # 使用套接字连接指定地址
        await loop.getaddrinfo(domain, None)
    except socket.gaierror:
        return (domain, False)
    return (domain, True)

async def main() -> None:
    names = (kw for kw in kwlist if len(kw) <= MAX_KEYWORD_LEN )
    domains = (f'{name}.dev'.lower() for name in names)
    # 提交多个任务到事件循环
    coros = [probe(domain) for domain in domains]
    # 按完成顺序获取结果
    for coro in asyncio.as_completed(coros):
        domain, found = await coro
        mark = '+' if found else ' '
        print(f'{mark:3} {domain}')

if __name__ == '__main__':
    asyncio.run(main())
