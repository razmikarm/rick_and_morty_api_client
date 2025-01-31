import json
from ramapi import Client


def main():
    api_client = Client()
    with open('result.json', 'w') as f:
        data = api_client.characters.filter(name='Garbage Goober', status='alive')
        json.dump(data, f, indent=4)


if __name__ == "__main__":
    main()
