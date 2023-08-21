import asyncio
import time

from sqlalchemy import select, func
from bot.utils.unit_of_work import UnitOfWork
from db import Links, User
# from db.base import create_async_session
from aiogram import Bot
from bot.config_data.config import config
from threading import Thread

bot: Bot = Bot(token=config.bot.token)







async def send_scheduler_msg():
    print("vmkemvcle")
    uow = UnitOfWork()
    async with uow:
        dora = await uow.links.find_random(is_dataset=True)
        if dora:
            dora.is_dataset = False
        else:
            dora = await uow.links.find_random(is_cool=True)
            if not dora:
                return

        d = {"is_dora": True}
        users = await uow.users.find_all(filters=d)
        for user in users:
            await bot.send_photo(user.user_id, photo=dora.file_id)
        await uow.commit()
        count = await uow.links.count_records(is_dataset=True)
        if count <= 5:
            await bot.send_message(config.bot.admin, f'Добавь фотки в датасет! Осталось {count}!')
