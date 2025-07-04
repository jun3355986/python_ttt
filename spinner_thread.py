import itertools
import time
from threading import Thread, Event

def spin(msg: str, done: Event) -> None:
    """
    这个函数的作用是：
    1. 使用itertools.cycle(r'\|/-') 生成一个循环的序列，用于在控制台中显示旋转的动画。
    2. 使用done.wait(.1) 等待100毫秒，然后检查done是否被设置为True。
    3. 如果done被设置为True，则退出循环。
    4. 否则，继续显示下一个字符。
    """
    for  char in itertools.cycle(r'\|/-'):
        status = f'\r{char} {msg}'
        print(status, end='', flush=True)
        if done.wait(1.1):
            break
    blanks = ' ' * len(status)
    # 打印空白行，覆盖之前的打印
    """
    1. \r 的作用
    \r 是回车符（carriage return），它的作用是把光标移动到当前行的开头，但不会换行。
    这样，后续的输出会从行首开始，覆盖掉原来这一行的内容。

    2. blanks 的作用
    blanks 是一串空格，长度和之前打印的内容一样长。
    这样做的目的是用空格把之前的字符“抹掉”，防止原内容残留。

    3. print(f'\r{blanks}\r', end='') 的完整流程
    第一个 \r：把光标移到行首。
    {blanks}：输出一串空格，把原有内容覆盖掉。
    第二个 \r：再次把光标移到行首，为后续新的输出（比如 Answer: 42）做好准备。
    end=''：不换行，光标还在当前行。
    """
    print(f'\r{blanks}\r', end='')

def slow() -> int:
    time.sleep(13)
    return 42

def supervisor() -> int:
    done = Event()
    spinner = Thread(target=spin, args=('thinking!', done))
    print(f'spinner object: {spinner}')
    # 启动spinner线程, 开始旋转
    spinner.start()
    # 执行耗时操作
    result = slow()
    
    # result = cpu_intensive_task()
    # 设置event为True，通知spin函数停止旋转
    # 把event设置为True，通知spin函数停止旋转
    done.set()
    # 等待spinner线程结束
    spinner.join()
    return result

def cpu_intensive_task() -> int:
    start_time = time.time()
    result = 1
    for i in range(1, 200000):
        result *= i
    end_time = time.time()
    print(f'耗时：{end_time - start_time: .2f}秒')
    return 88

def main() -> None:
    result = supervisor()
    print(f'Answer: {result}')

if __name__ == '__main__':
    main()