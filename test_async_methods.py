import asyncio
import time

import httpx
import requests

URL = "https://www.tradamuse.fr/content/images/size/w2000/2020/03/IMG_0667.jpg"


async def download_something_big_async(my_str):
    start_time = time.perf_counter()
    print(f"start: {my_str}")
    with open(f"/tmp/test_asyncio_download.{my_str}.tmp", "wb") as fd:
        async with httpx.AsyncClient() as client:
            async with client.stream("GET", URL) as r:
                async for chunk in r.aiter_bytes():
                    fd.write(chunk)
    print(f"finished: {my_str} in {time.perf_counter() - start_time}s")


async def download_something_big(my_str):
    start_time = time.perf_counter()
    print(f"start: {my_str}")
    with open(f"/tmp/test_asyncio_download.{my_str}.tmp", "wb") as fd:
        r = requests.get(URL, stream=True)
        for chunk in r.iter_content():
            fd.write(chunk)
    print(f"finished: {my_str} in {time.perf_counter() - start_time}s")


async def main():
    start_time = time.perf_counter()
    print("Start main ...")
    method = download_something_big_async
    await asyncio.wait(
        [method("A"), method("B"), method("C")],
        return_when=asyncio.ALL_COMPLETED,
        timeout=60,
    )
    print(f"... total : {time.perf_counter() - start_time}s the end!")


asyncio.run(main())
