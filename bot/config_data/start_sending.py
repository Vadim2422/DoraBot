from sqlalchemy import select, func

from bot.utils.unit_of_work import UnitOfWork
from main import scheduler
from db import Links, User
# from db.base import create_async_session
from aiogram import Bot
from bot.config_data.config import config

bot: Bot = Bot(token=config.bot.token)


def start_sending_msg():
    if not scheduler.running:
        scheduler.add_job(send_scheduler_msg, trigger='cron', hour='*', minute='0', id="start")
        scheduler.start()


async def send_scheduler_msg():
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
