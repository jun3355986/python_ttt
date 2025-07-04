import math
import time
import asyncio
from typing import Callable

NUMBERS = [ 2,
            142_702_110_479_723,
            299_593_572_317_531,    
            333_333_333_333_3301,
            333_333_333_333_3333,
            333_333_565_209_2209,
            444_444_444_444_4423,
            444_444_444_444_4444,
            444_444_448_888_8889,
            555_555_313_314_9889,
            555_555_555_555_5503,
            555_555_555_555_5555,
            666_666_666_666_6666,
            666_666_666_666_6719,
            666_666_714_141_4921,
            777_777_753_634_0681,
            777_777_777_777_7753,
            777_777_777_777_7777,
            999_999_999_999_9917,
            999_999_999_999_9999]

def is_prime(n: int) -> bool:
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    
    # 计算n的平方根
    root = math.isqrt(n)
    for i in range(3, root + 1, 2):
        if n % i == 0:
            return False
    
    return True

async def is_prime_async(n: int) -> bool:
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    
    # 计算n的平方根
    root = math.isqrt(n)
    for i in range(3, root + 1, 2):
        if n % i == 0:
            return False
        if i % 100_000 == 1:
            await asyncio.sleep(0)
    
    return True


def print_time(func: Callable, n: int):
    start_time = time.time()

    func(n)
    func(n)
    print(func(n))

    print(f"Time token: {time.time() - start_time} 秒")

async def print_time_async(func: Callable, n: int):
    start_time = time.time()

    # await func(n)
    # await func(n)
    print(await func(n))

    print(f"Time token: {time.time() - start_time} 秒")
