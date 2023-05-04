import json
import os.path
import random
import base64
from bot.errors.photos_are_over import PhotosAreOverError
import aiohttp

from bot.files.json_files import add_photo_to_, delete_photo_from_


class Photo:
    link: str
    count_current_photo: int = -1

    def __init__(self):
        try:
            with open('src/current_photo.json', 'r') as file:
                data = json.load(file)
                self.link = data['link']
                self.count_current_photo = data['count_current_photo']

        except Exception:
            self.add_new_photo()

    def add_new_photo(self):
        with open('src/links.json', 'r') as file:
            links: list = json.load(file)
            if not len(links):
                raise PhotosAreOverError
            rand = random.randint(0, len(links) - 1)
        self.link = links[rand]
        self.count_current_photo += 1
        self.save()

    def add_photo_to_trash(self):
        add_photo_to_('src/trash.json', self.link)
        self.delete_from_links()
        self.add_new_photo()

    def add_photo_to_dataset(self):
        add_photo_to_('src/dataset.json', self.link)
        add_photo_to_('src/cool_photo.json', self.link)
        self.delete_from_links()
        self.add_new_photo()

    def save(self):
        with open('src/current_photo.json', 'w') as file:
            json.dump(self.__dict__, file, indent=4)

    def delete_from_links(self) -> None:
        delete_photo_from_('src/links.json', self.link)


    def delete_from_dataset(self, link) -> None:
        delete_photo_from_('src/dataset.json', link)
        if self.count_current_photo:
            self.count_current_photo -= 1
            self.save()



    async def download_photo(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(self.link) as resp:
                resp_dict = await resp.content.read()
        return resp_dict

        # with open(f'src/photos/{base64.b64encode(self.link)}.jpeg'):
