import sys
from time import perf_counter
from typing import NamedTuple
from multiprocessing import Process, SimpleQueue, cpu_count
from multiprocessing import queues
from threading import Thread

from my_primes import is_prime, NUMBERS

"""
结论：
python里多线程可以并发处理任务， 但是thread的多线程处理任务时跟cpu核心数线程数多少无关。
在cpu密集型任务中，thread的多线程处理任务时，性能不如多进程。而且线程数越多，性能越差。
"""

class PrimeResult(NamedTuple):
    n: int
    prime: bool
    elapsed: float

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
        proc = Thread(target=worker, args=(jobs, results))
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