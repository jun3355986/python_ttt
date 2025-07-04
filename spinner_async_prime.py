import asyncio
import itertools
import time
from my_primes import is_prime, print_time

def main() -> None:
    result = asyncio.run(supervisor())
    print(f'Answer: {result}')

async def supervisor() -> int:
    # 创建spinner任务, 会自动在后台运行spin函数
    spinner = asyncio.create_task(spin('thinking!'))
    print(f'spinner object: {spinner}')
    # 等待slow函数完成, 期间spinner会继续运行
    result = await slow()
    # 取消spinner任务, 会触发spin函数中的CancelledError异常, 从而退出循环
    spinner.cancel()
    return result

async def spin(msg: str) -> None:
    for char in itertools.cycle(r'\|/-'):
        status = f'\r{char} {msg}'
        print(status, end='', flush=True)
        try:
            await asyncio.sleep(.1)
        except asyncio.CancelledError:
            break
    blanks = ' ' * len(status)
    print(f'\r{blanks}\r', end='')

async def slow() -> int:
    # await asyncio.sleep(5)
    # time.sleep(5)
    print_time(is_prime, 50_000_111_000_222_021)
    return 42


if __name__ == '__main__':
    main()
