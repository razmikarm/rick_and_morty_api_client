import requests
from ramapi.resource import Resource

class Client:

    characters: Resource
    locations: Resource
    episodes: Resource

    def __init__(self, base_url: str = "https://rickandmortyapi.com/api/") -> None:
        self.url = base_url.rstrip('/')
        self.resources = dict()
        self.__gen_resources()

    def get_available_resources(self) -> dict:
        return requests.get(self.url).json()

    def __gen_resources(self) -> None:
        resources = self.get_available_resources()
        for res_name, res_url in resources.items():
            res_object =  Resource(res_url)
            self.resources[res_name] = res_object
            setattr(self, res_name, res_object)

    def fetch_all_resources(self) -> dict:        
        result = dict()
        for res_name, res in self.resources.items():
            result[res_name] = res.get_all()
        return result
