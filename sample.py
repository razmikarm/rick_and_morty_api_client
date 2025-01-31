import json
from uuid import uuid4

from ramapi import Client
from ramapi.utils import ep_aired_between


def save_json(filename, data: dict) -> None:
    with open(f'{filename}.json', 'w') as f:
        content = {"id": str(uuid4()), "RawData": data}
        json.dump(content, f, indent=4)

def main() -> None:
    api_client = Client()
    all_res_data = api_client.fetch_all_resources()
    for res_name, res_data in all_res_data.items():
        save_json(res_name, res_data)

    start_year, end_year = 2017, 2021
    filter_func = ep_aired_between(start_year, end_year)
    filtered_episodes = filter(filter_func, all_res_data["episodes"])
    print(f"Episodes aired between {start_year} and {end_year}:")
    [print(f'- {ep["name"]}') for ep in filtered_episodes]


if __name__ == "__main__":
    main()
