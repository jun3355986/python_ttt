import time
from pathlib import Path
from typing import Callable

import httpx

POP20_CC = ('CH IN US ID BR PK NG BD RU JP '
           'MX PH VN ET EG DE IR TR CD FR').split()

BASE_URL2 = 'https://www.fluentpython.com/data/flags'
BASE_URL = 'http://mp.ituring.com.cn/files/flags'

DEST_DIR = Path('downloads')

def save_flag(img: bytes, filename: str) -> None:
    # 把bytes的图片保存到指定目录
    (DEST_DIR / filename).write_bytes(img)

def get_flag(cc: str) -> bytes:
    url = f'{BASE_URL}/{cc}/{cc}.gif'.lower()
    resp = httpx.get(url, timeout=6.1, follow_redirects = True)
    # 如果请求响应不是2xx，抛出异常
    resp.raise_for_status()
    return resp.content

def download_many(cc_list: list[str]) -> int:
    for cc in sorted(cc_list):
        image = get_flag(cc)
        save_flag(image, f'{cc}.gif')
        print(cc, end=' ', flush=True)

    return len(cc_list)
    
def main(downloader: Callable[[list[str]], int]) -> None:
    # 如果目录不存在，则创建目录
    DEST_DIR.mkdir(exist_ok=True)
    t0 = time.perf_counter()
    count = downloader(POP20_CC)
    elapsed = time.perf_counter() - t0
    print(f'\n{count} downloads in {elapsed:.2f}s')

if __name__ == '__main__':
    main(download_many)