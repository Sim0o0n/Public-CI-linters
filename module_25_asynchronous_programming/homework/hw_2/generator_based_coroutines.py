import asyncio
import time
import requests
from pathlib import Path

URL = 'https://cataas.com/cat'
OUT_PATH = Path(__file__).parent / 'cats'
OUT_PATH.mkdir(exist_ok=True, parents=True)
OUT_PATH = OUT_PATH.absolute()

async def download_cat(idx):
    response = await asyncio.to_thread(requests.get, URL)
    with open(OUT_PATH / f"cat_{idx}.png", 'wb') as f:
        f.write(response.content)

async def download_cats(num_cats):
    tasks = [download_cat(i) for i in range(num_cats)]
    await asyncio.gather(*tasks)

if __name__ == '__main__':
    for num_cats in [10, 50, 100]:
        start_time = time.time()
        asyncio.run(download_cats(num_cats))
        print(f"Time taken (async) for {num_cats} cats: {time.time() - start_time:.2f} seconds")


