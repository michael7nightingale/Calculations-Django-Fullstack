from django.test import TestCase
from aiohttp import ClientSession
import asyncio
import time


async def test(url: str, n_request: int):
    time_started = time.perf_counter()
    async with ClientSession() as session:
        for _ in range(n_request):
            async with session.get(url) as response:
                res = await response.text()
        print(res)

    print(time.perf_counter() - time_started)


if __name__ == '__main__':
    url_ = "http://127.0.0.1:8000/api/v1"
    asyncio.run(test(url_, 1000))
