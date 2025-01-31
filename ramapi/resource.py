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
            page_data = self.get_page(page)
            results.extend(page_data["results"])
        return results

    def get_page(self, page: int) -> dict:
        target_url = f'{self.url}?page={page}'
        return requests.get(target_url).json()

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
