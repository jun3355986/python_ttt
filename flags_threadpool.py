from concurrent import futures
from flags import save_flag, get_flag, main

def download_one(cc: str) -> None:
    image = get_flag(cc)
    save_flag(image, f'{cc}.gif')
    print(cc, end=' ', flush=True)
    return cc

def download_many(cc_list: list[str]) -> int:
    with futures.ThreadPoolExecutor() as executor:
        # 提交线程池，按顺序执行download_one函数，并返回结果
        res = executor.map(download_one, sorted(cc_list))

    return len(list(res))

if __name__ == '__main__':
    main(download_many)