import asyncio

from sqlalchemy.ext.asyncio import AsyncSession

from bot.config_data.config import load_config
import json
import aiohttp

from db import Dora
from db.postges.postgres_base import create_async_session
config = load_config()
base_url: str = 'https://api.vk.com/method/'
method: str = 'photos.get'
owner_id: str = '-191792737'
album_id: str = 'wall'
token: str = config.vk_token
api_v: str = '5.131'


async def get_id(link: str) -> int:
    async with aiohttp.ClientSession() as session:
        async with session.get(base_url + 'utils.resolveScreenName', params={
            'screen_name': link.replace('https://', '').replace('vk.com/', ''),
            'access_token': token,
            'v': api_v
        }) as resp:
            return json.loads(await resp.content.read())['response']['object_id']


async def get_resp(owner_id: int = owner_id, count: int = 1000, offset: int = 0, rev: int = 1):
    async with aiohttp.ClientSession() as session:
        async with session.get(base_url + method, params={
            'owner_id': f'-{owner_id}',
            'album_id': album_id,
            'count': count,
            'offset': offset,
            'rev': rev,
            'access_token': token,
            'v': api_v
        }) as resp:
            return json.loads(await resp.content.read())


def get_max_size(item: dict) -> str:
    max_size: int = 0
    link: str = ''
    for size in item['sizes']:
        if size['height'] > max_size:
            link = size['url']
            max_size = size['height']
    return link


async def get_all_photo(link: str):
    links: list[str] = []
    offset: int = 0

    tasks = []
    owner_id = await get_id(link)
    response = await get_resp(owner_id=owner_id)
    count = response['response']['count']

    while count > offset:
        tasks.append(asyncio.create_task(get_resp(owner_id=owner_id, offset=offset)))
        offset += 1000
    responses = await asyncio.gather(*tasks)
    for response in responses:
        for item in response['response']['items']:
            links.append(get_max_size(item))
    links = list(dict.fromkeys(links))
    dora_links: list[Dora] = []
    for no_repeat_link in links:
        dora_links.append(Dora(link=no_repeat_link))
    # Dora(link=)
    Session = create_async_session()
    async with Session() as session:
        session: AsyncSession
        session.add_all(dora_links)
        await session.commit()
    # with open('src/links.json', 'w') as file:
    #     json.dump(links, file, indent=4)
