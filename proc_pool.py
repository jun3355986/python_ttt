import sys
from time import perf_counter
from typing import NamedTuple
from multiprocessing import Process, SimpleQueue, cpu_count
from multiprocessing import queues
from concurrent import futures

from my_primes import is_prime, NUMBERS

"""
procs.py的代替版， 使用concurrent.futures.ProcessPoolExecutor

结论：
python里多进程可以并行处理任务，一般情况下使用核心数越多，性能越好。
但是，超过最大核心数，性能变化不大甚至下降。
"""

class PrimeResult(NamedTuple):
    n: int
    prime: bool
    elapsed: float

"""
SimpleQueue 是一个线程安全、进程安全的队列，底层用管道（Pipe）和锁（Lock）实现

特性
1.进程安全：多个进程可以同时往队列里放数据（put）或取数据（get），不会数据错乱。
2.先进先出（FIFO）：先放入的元素先被取出。
3.无大小限制：理论上可以无限放数据（受内存限制）。
4.阻塞/非阻塞：get() 默认会阻塞直到有数据可取，也可以设置超时或非阻塞。
5.跨进程共享：只要队列对象传给多个进程，大家都能访问同一个队列。

"""
JobQueue = queues.SimpleQueue[int]
ResultQueue = queues.SimpleQueue[PrimeResult]

def check(n: int) -> PrimeResult:
    t0 = perf_counter()
    res = is_prime(n)
    return PrimeResult(n, res, perf_counter() - t0)

def worker(jobs: JobQueue, results: ResultQueue) -> None:
    while n := jobs.get():
        results.put(check(n))
    # 这一行干嘛用的？
    # 这一行是每个进程结束时，向结果队列中添加一个结束标志，用于标识该进程已经结束；后面report函数会根据这个标志来判断进程是否结束。
    results.put(PrimeResult(0, False, 0.0))


def main() -> None:
    if len(sys.argv) < 2:
        workers = None
    else:
        workers = int(sys.argv[1])
    
    executor =futures.ProcessPoolExecutor(workers)
    actual_workers = executor._max_workers # type: ignore

    print(f'Checking {len(NUMBERS)} numbers with {actual_workers} processes:')

    t0 = perf_counter()

    numbers = sorted(NUMBERS, reverse = True)

    with executor:
        # 进程返回的结果是按提交顺序返回的，不是按数字大小返回的，当排序在前的执行时间比较长，会阻塞返回结果，不过此时后面的进程会继续执行。
        for n, prime, elapsed in executor.map(check, numbers):
            label = 'P' if prime else ' '
            print(f'{n:16} {label} {elapsed:9.6f}s')

        time = perf_counter() - t0
        print(f'Total time: {time:.2f}s')


if __name__ == '__main__':
    main()