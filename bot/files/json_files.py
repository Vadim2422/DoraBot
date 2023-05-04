import asyncio
import json
import pathlib

from parsing.parsing import get_all_photo


def create_files():
    files_path = ['src/current_photo.json', 'src/cool_photo.json', 'src/dataset.json', 'src/send_users.json']
    for path in files_path:
        create_file(path)




def create_file(path):
    if not pathlib.Path(path).is_file():
        with open(path, 'w') as file:
            file.write('[]')


def add_photo_to_(path: str, link: str) -> None:
    try:
        with open(path, 'r') as file:
            links: list = json.load(file)
            if link not in links:
                links.append(link)

    except Exception:
        links = [link]
    finally:
        with open(path, 'w') as file:
            json.dump(links, file, indent=4)


def delete_photo_from_(path: str, link: str) -> None:
    try:
        with open(path, 'r') as file:
            links: list = json.load(file)
            links.remove(link)

    except Exception:
        links = []
    finally:
        with open(path, 'w') as file:
            json.dump(links, file, indent=4)

def get_links_from_file(path):
    with open(path, 'r') as file:
        return json.load(file)


def get_send_users():
    return get_links_from_file('src/send_users.json')


def get_dataset():
    return get_links_from_file('src/dataset.json')


def get_cool():
    return get_links_from_file('src/cool_photo.json')

def get_links():
    return get_links_from_file('src/links.json')
