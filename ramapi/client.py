import requests
from ramapi.resource import Resource

class Client:

    characters: Resource
    locations: Resource
    episodes: Resource

    def __init__(self, base_url: str = "https://rickandmortyapi.com/api/") -> None:
        self.url = base_url.rstrip('/')
        self.__gen_resources()

    def resources(self) -> dict:
        return requests.get(self.url).json()

    def __gen_resources(self) -> None:
        resources = requests.get(self.url).json()
        for res_name, res_url in resources.items():
            setattr(self, res_name, Resource(res_url))
