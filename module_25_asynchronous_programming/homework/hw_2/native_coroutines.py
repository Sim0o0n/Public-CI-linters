import requests
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import time

URL = 'https://cataas.com/cat'
CATS_WE_WANT_LIST = [10, 50, 100]
OUT_PATH = Path(__file__).parent / 'cats'
OUT_PATH.mkdir(exist_ok=True, parents=True)
OUT_PATH = OUT_PATH.absolute()

# Функция для загрузки котика
def download_cat(idx):
    response = requests.get(URL)
    with open(OUT_PATH / f"cat_{idx}.png", 'wb') as f:
        f.write(response.content)

# Загрузка котиков с использованием тредов
def download_cats_threaded(num_cats):
    with ThreadPoolExecutor() as executor:
        executor.map(download_cat, range(num_cats))

# Загрузка котиков с использованием процессов
def download_cats_multiprocess(num_cats):
    with ProcessPoolExecutor() as executor:
        executor.map(download_cat, range(num_cats))

if __name__ == '__main__':
    for num_cats in CATS_WE_WANT_LIST:
        # Измерение времени для тредов
        start_time = time.time()
        download_cats_threaded(num_cats)
        print(f"Time taken (threads) for {num_cats} cats: {time.time() - start_time:.2f} seconds")

        # Измерение времени для процессов
        start_time = time.time()
        download_cats_multiprocess(num_cats)
        print(f"Time taken (processes) for {num_cats} cats: {time.time() - start_time:.2f} seconds")
