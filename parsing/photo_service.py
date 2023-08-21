import asyncio
import io

from sqlalchemy.ext.asyncio import AsyncSession

from bot.config_data.config import config
import json
import aiohttp

from bot.services.base_service import BaseService
from db import Links


class PhotoService(BaseService):
    base_url: str = 'https://api.vk.com/method/'
    group_album_id: int = 295897951
    group_id: int = 174635541
    user_album_id: int = 295874718
    owner_id: str = '-191792737'
    album_id: str = 'wall'
    user_token: str = config.vk.user_token
    api_v: str = config.vk.api_v

    async def get_id(self, link: str) -> int:
        async with aiohttp.ClientSession() as session:
            async with session.get(self.base_url + 'utils.resolveScreenName', params={
                'screen_name': link.replace('https://', '').replace('vk.com/', ''),
                'access_token': self.user_token,
                'v': self.api_v
            }) as resp:
                return (await resp.json())['response']['object_id']

    @classmethod
    async def get_upload_group_server(cls):
        async with aiohttp.ClientSession() as session:
            async with session.get(cls.base_url + 'photos.getUploadServer', params={
                'album_id': cls.group_album_id,
                'group_id': cls.group_id,
                'access_token': cls.user_token,
                'v': cls.api_v
            }) as resp:
                return (await resp.json())['response']['upload_url']

    @classmethod
    async def get_upload_user_server(cls):
        async with aiohttp.ClientSession() as session:
            async with session.get(cls.base_url + 'photos.getUploadServer', params={
                'album_id': cls.user_album_id,
                'access_token': cls.user_token,
                'v': cls.api_v
            }) as resp:
                return (await resp.json())['response']['upload_url']

    @classmethod
    async def upload_photo_on_server(cls, upload_url, photo_link):
        async with aiohttp.ClientSession() as session:
            async with session.get(photo_link) as photo_resp:
                file_name = photo_resp.url.name
                data = aiohttp.FormData()
                data.add_field('file1', photo_resp.content, filename=file_name)
                async with session.post(upload_url, data=data) as resp:
                    return json.loads(await resp.content.read())

    @classmethod
    async def save_photo_to_group_album(cls, server: int, photos_list: str, hash_: str):
        async with aiohttp.ClientSession() as session:
            params = {'album_id': cls.group_album_id,
                      'group_id': cls.group_id,
                      'server': server,
                      'photos_list': photos_list,
                      'hash': hash_,
                      'access_token': cls.user_token,
                      'v': cls.api_v}
            async with session.get(cls.base_url + "photos.save", params=params) as resp:
                return (await resp.json())['response'][0]

    @classmethod
    async def save_photo_to_user_album(cls, server: int, photos_list: str, hash_: str):
        async with aiohttp.ClientSession() as session:
            params = {'album_id': cls.user_album_id,
                      'server': server,
                      'photos_list': photos_list,
                      'hash': hash_,
                      'access_token': cls.user_token,
                      'v': cls.api_v}
            async with session.get(cls.base_url + "photos.save", params=params) as resp:
                return (await resp.json())['response'][0]

    @classmethod
    async def move_photo(cls, owner_id: int, photo_id: int):
        params = {'owner_id': owner_id,
                  'target_album_id': cls.user_album_id,
                  'photo_id': photo_id,
                  'access_token': cls.user_token,
                  'v': cls.api_v}
        async with aiohttp.ClientSession() as session:
            async with session.get(cls.base_url + "photos.move", params=params) as resp:
                res = await resp.json()
                print(res)

    @classmethod
    async def add_photo_to_vk_album(cls, link_photo):
        group_upload_url = await cls.get_upload_group_server()
        server_data = await cls.upload_photo_on_server(group_upload_url, link_photo)
        photo = await cls.save_photo_to_group_album(server_data['server'],
                                                    server_data['photos_list'],
                                                    server_data['hash'])

        user_upload_url = await cls.get_upload_user_server()
        server_data = await cls.upload_photo_on_server(user_upload_url, link_photo)
        photo = await cls.save_photo_to_user_album(server_data['server'],
                                                   server_data['photos_list'],
                                                   server_data['hash'])

    @classmethod
    async def get_resp(cls, owner_id: int = owner_id, count: int = 1000, offset: int = 0, rev: int = 1):
        async with aiohttp.ClientSession() as session:
            async with session.get(cls.base_url + 'photos.get', params={
                'owner_id': f'-{owner_id}',
                'album_id': cls.album_id,
                'count': count,
                'offset': offset,
                'rev': rev,
                'access_token': cls.user_token,
                'v': cls.api_v
            }) as resp:
                return json.loads(await resp.content.read())

    def get_max_size(self, item: dict) -> str:
        max_size: int = 0
        link: str = ''
        for size in item['sizes']:
            if size['height'] > max_size:
                link = size['url']
                max_size = size['height']
        return link

    async def get_all_photo(self, link: str):
        links: list[str] = []
        offset: int = 0

        tasks = []
        owner_id = await self.get_id(link)
        response = await self.get_resp(owner_id=owner_id)
        count = response['response']['count']

        while count > offset:
            tasks.append(asyncio.create_task(self.get_resp(owner_id=owner_id, offset=offset)))
            offset += 1000
        responses = await asyncio.gather(*tasks)
        for response in responses:
            for item in response['response']['items']:
                links.append(self.get_max_size(item))
        no_repeat_links = set(links)
        dora_links: list[Links] = []
        for link in no_repeat_links:
            dora_links.append(Links(link=link))
        await self.add_photo_to_db(dora_links)
        # for link in no_repeat_links:
        #     await self.add_photo_to_db(Links(link=link))

    async def add_photo_to_db(self, link_db):
        async with self.uow:
            await self.uow.links.add_all(link_db)
            await self.uow.commit()
