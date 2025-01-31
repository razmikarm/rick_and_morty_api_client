import requests

import asyncio
import urllib.parse
from aiohttp import ClientSession


class Resource:

    def __init__(self, base_url: str) -> None:
        self.url = base_url.rstrip('/')

    def get(self) -> dict:
        result = requests.get(self.url).json()
        return result

    async def fetch_all_async(self) -> list:
        page_count = self.get()["info"]["pages"]
        async with ClientSession() as session:
            tasks = [self.fetch_page_async(session, page) for page in range(1, page_count + 1)]
            pages = await asyncio.gather(*tasks)
            flattened = [res for data in pages for res in data["results"]]
            return flattened

    def fetch_all(self) -> list:
        return asyncio.run(self.fetch_all_async())

    async def fetch_page_async(self, session: ClientSession, page: int) -> dict:
        target_url = f'{self.url}?page={page}'
        async with session.get(target_url) as response:
            return await response.json()

    def fetch_page(self, page: int) -> dict:
        async def inner():
            async with ClientSession() as session:
                return await self.fetch_page_async(session, page)
        return asyncio.run(inner())

    def get_by_ids(self, *ids: list) -> dict:
        if len(ids) == 0:
            raise ValueError("At least one id must be given")
        elif len(ids) == 1:
            id = ids[0]
        else:
            id = ','.join([str(i) for i in ids])
        target_url = f"{self.url}/{id}"
        return requests.get(target_url).json()

    def filter(self, **params: dict) -> dict:
        query = urllib.parse.urlencode(params)
        target_url = f"{self.url}?{query}"
        return requests.get(target_url).json()
