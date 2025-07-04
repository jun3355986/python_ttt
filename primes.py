import math
import time

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


def print_time(n: int):
    start_time = time.time()

    print(is_prime(n))

    print(f"Time token: {time.time() - start_time} 秒")
