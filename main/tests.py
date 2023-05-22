import asyncio
import time

from django.test import TestCase
from urllib import request, response
import aiohttp


# url = 'http://localhost:8000/science/physics/'
# req = request.Request(
#     url=url,
#     method="GET",
#     headers={'Content-Type': "text/html"}
# )


async def test_url(url: str, n_requests: int) -> float:
    time_start = time.perf_counter()
    async with aiohttp.ClientSession() as session:
        try:
            for n in range(n_requests):
                async with session.get(url) as response:
                    text = await response.text()
        except Exception as e:
            print(str(e))
        finally:
            return time.perf_counter() - time_start


time_physics = asyncio.run(
    test_url('http://localhost:8000/', 1000)
)
print(time_physics)
