import itertools
import time
from multiprocessing import Process, Event
from multiprocessing import synchronize
from my_primes import is_prime, print_time

def spin(msg: str, done: synchronize.Event) -> None:
    for char in itertools.cycle(r'\|/-'):
        status = f'\r{char} {msg}'
        print(status, end='', flush=True)
        if done.wait(.1):
            break
    blanks = ' ' * len(status)
    print(f'\r{blanks}\r', end='')

def supervisor() -> int:
    done = Event()
    spinner = Process(target=spin, args=('thinking!', done))
    print(f'spinner object: {spinner}')
    spinner.start()
    result = slow()   
    done.set()
    spinner.join()
    return result

def slow() -> int:
    # time.sleep(3)
    print_time(is_prime, 50_000_111_000_222_021)
    return 42

def main() -> None:
    result = supervisor()
    print(f'Answer: {result}')

if __name__ == '__main__':
    main()