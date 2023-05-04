import asyncio
import datetime

from sqlalchemy import select, func

from db import Dora, User
from db.postges.postgres_base import create_async_session
from aiogram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from bot.config_data.config import config

bot: Bot = Bot(token=config.bot.token)


def start_sending_msg():
    scheduler = AsyncIOScheduler(timezone="Europe/Moscow")
    scheduler.add_job(send_test_msg, trigger='cron', hour='*', minute=0)
    scheduler.start()


async def send_test_msg():
    session = create_async_session()
    async with session() as session:
        stmt = select(Dora).where(Dora.is_dataset == True).order_by(func.random()).limit(1)
        dora = await session.scalar(stmt)
        if not dora:
            return
        dora.is_dataset = False
        await session.commit()
        stmt = select(User).where(User.is_dora == True)
        for user in await session.scalars(stmt):
            await bot.send_photo(user.user_id, photo=dora.file_id)
        stmt = select(func.count()).where(Dora.is_dataset == True).select_from(Dora)
        count = await session.scalar(stmt)
        if count <= 5:
            await bot.send_message(config.bot.admin, f'Добавь фотки в датасет! Осталось {count} фотографий!')
