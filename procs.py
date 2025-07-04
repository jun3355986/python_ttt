import sys
from time import perf_counter
from typing import NamedTuple
from multiprocessing import Process, SimpleQueue, cpu_count
from multiprocessing import queues

from my_primes import is_prime, NUMBERS

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

def start_jobs( procs: int, jobs: JobQueue, results: ResultQueue) -> None:
    for n in NUMBERS:
        jobs.put(n)
    for _ in range(procs):
        proc = Process(target=worker, args=(jobs, results))
        proc.start()
        # 这一行干嘛用的？
        # 这一行向jobs里放一个 0，在worker函数中，如果n为0，则表示该进程结束。
        jobs.put(0)

def main() -> None:
    if len(sys.argv) < 2:
        procs = cpu_count()
    else:
        procs = int(sys.argv[1])
    print(f'Checking {len(NUMBERS)} numbers with {procs} processes:')
    t0 = perf_counter()
    # 这里为什么这么写，代表什么意思？
    jobs: JobQueue = SimpleQueue()
    results: ResultQueue = SimpleQueue()
    start_jobs(procs, jobs, results)
    checked = report(procs, results)
    elapsed = perf_counter() - t0
    print(f'{checked} checks in {elapsed:.2f}s')

def report(procs: int, results: ResultQueue) -> int:
    checked = 0
    procs_done = 0
    while procs_done < procs:
        n, prime, elapsed = results.get()
        if n == 0:
            procs_done += 1
        else:
            checked += 1
            label = 'P' if prime else ' '
            print(f'{n:16}  {label}  {elapsed:9.6f}s')
    return checked

if __name__ == '__main__':
    main()