import asyncio
import random

import aiohttp

import json

from aiogram import Bot
from aiogram.types import InputFile

from bot.config_data.photo import Photo
from bot.files.json_files import get_send_users, get_dataset, get_cool, get_links


async def send_user(bot: Bot, photo):
    while True:
        dataset = get_dataset()
        if not dataset:
            dataset = get_cool()
        if not dataset:
            dataset = get_links()
        link = dataset[random.randint(0, len(dataset) - 1)]
        async with aiohttp.ClientSession() as session:
            async with session.get(link) as resp:
                resp_dict = await resp.content.read()
        users = get_send_users()
        for user in users:
            await bot.send_photo(chat_id=user, photo= resp_dict)
        photo.delete_from_dataset(link)
        await asyncio.sleep(5)


async def send_admin(bot: Bot, photo: Photo):
    await bot.send_photo(chat_id=889732033, photo=await photo.download_photo(),
                         caption=f'Фото в датасете: {photo.count_current_photo}',
                         reply_markup=get_admin_ikb())
