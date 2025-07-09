from concurrent import futures
from flags import save_flag, get_flag, main

def download_one(cc: str) -> None:
    image = get_flag(cc)
    save_flag(image, f'{cc}.gif')
    print(cc, end=' ', flush=True)
    return cc

def download_many(cc_list: list[str]) -> int:
    cc_list = cc_list[:5]
    with futures.ThreadPoolExecutor(max_workers=3) as executor:
        to_do: list[futures.Future] = []
        for cc in sorted(cc_list):
            # 提交任务到线程池，返回一个Future对象
            future = executor.submit(download_one, cc)
            to_do.append(future)
            print(f'Scheduled for {cc}: {future}')

        # 遍历Future对象，获取结果
        """
        futures.as_completed(to_do) 是 concurrent.futures 模块提供的一个生成器函数。
        它会按任务完成的顺序，依次返回已经完成的 Future 对象（而不是你提交任务的顺序）。
        这样你可以在任务完成时立即处理结果，而不用等所有任务都完成。
        """
        for count, future in enumerate(futures.as_completed(to_do), 1):
            # 获取结果, 阻塞等待任务完成
            res: str = future.result()
            print(f'{future} result: {res!r}')
    
    return count

if __name__ == '__main__':
    main(download_many)