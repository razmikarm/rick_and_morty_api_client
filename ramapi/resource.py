import requests
import urllib.parse


# TODO: Replace `requests` with `aiohttp`
class Resource:

    def __init__(self, base_url: str) -> None:
        self.url = base_url.rstrip('/')

    def get(self) -> dict:
        result = requests.get(self.url).json()
        return result

    def get_all(self) -> list:
        page_count = self.get()["info"]["pages"]
        results = []
        for page in range(1, page_count + 1):
            page_data = self.get_pages(page)
            results.extend(page_data["results"])
        return results

    def get_pages(self, *pages: list) -> dict:
        if len(pages) == 0:
            raise ValueError("At least one page number must be given")
        elif len(pages) == 1:
            page = pages[0]
        else:
            page = ','.join([str(p) for p in pages])
        target_url = f'{self.url}?page={page}'
        return requests.get(target_url).json()

    def get_by_id(self, id: int) -> dict:
        target_url = f"{self.url}/{id}"
        return requests.get(target_url).json()

    def filter(self, **params: dict) -> dict:
        query = urllib.parse.urlencode(params)
        target_url = f"{self.url}?{query}"
        return requests.get(target_url).json()
