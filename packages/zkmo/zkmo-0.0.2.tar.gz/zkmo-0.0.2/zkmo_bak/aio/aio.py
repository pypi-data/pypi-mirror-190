import time
import asyncio
from typing import List

from loguru import logger

import httpx


class AIORequest:

    async def get(self, url):
        return await self._request("GET", url)

    async def _request(self, method, url, **kwargs):
        async with httpx.AsyncClient() as client:
            response = await client.request(method, url=url)
            logger.info(f"response time: {response.elapsed.total_seconds()}")
            data = response.json()
            logger.info(data)
            return data


aio_request = AIORequest()


async def get_data(field):
    url = f"http://httpbin.org/{field}"
    return await aio_request.get(url)


def concurrent_run_aio_tasks(tasks: List[tuple]):
    logger.info("")
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    works = []
    for task in tasks:
        func = task[0]
        args, kwargs = (), {}
        if len(task) > 1:
            args = task[1]
        if len(task) > 2:
            kwargs = task[2]
        works.append(asyncio.ensure_future(func(*args, **kwargs)))
    try:
        results = loop.run_until_complete(asyncio.gather(*works))
        logger.info(results)
    finally:
        loop.close()
    logger.info(time.time())


if __name__ == '__main__':
    concurrent_run_aio_tasks([(get_data, ("ip",)), (get_data, ("headers",))])
