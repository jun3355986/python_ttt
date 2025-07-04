#! /usr/bin/env python3
"""
Sequential.py : CPU 密集型工作的顺序执行版本、多进程版本和多线程版本的比较基准
"""

from time import perf_counter
from typing import NamedTuple

from my_primes import is_prime, NUMBERS

class Result( NamedTuple):
    prime: bool
    elapsed: float

def check(n: int) -> Result:
    # 高精度计时器，计时不受系统时钟频率影响，返回秒
    t0 = perf_counter()
    prime = is_prime(n)
    return Result(prime, perf_counter() - t0)

def main() -> None:
    print(f'Checking {len(NUMBERS)}  numbers  sequentially:')
    t0 = perf_counter()
    for n in NUMBERS:
        prime, elapsed = check(n)
        label = 'P' if prime else ' '
        print(f'{n:16}  {label}  {elapsed:9.6f}s')

    elapsed = perf_counter() -t0
    print(f'Total time: {elapsed:.2f}s')

if __name__ == '__main__':
    main()