import asyncio
import json
import os.path
from alembic import command
from alembic.config import Config
import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram import Bot, Dispatcher

from bot.config_data.schedule_sending import send_scheduler_msg
from bot.middlewares.db_middleware import DBMiddleware
from bot.config_data.config import config
from bot.handlers import user_handlers, admin_handlers

from bot.utils.unit_of_work import UnitOfWork

from bot.utils.comands import set_commands
from db.models import Admin
from flask_service.service import start_thread_flask
from logs.logger import logger
from parsing.photo_service import PhotoService

bot: Bot = Bot(token=config.bot.token)
dp: Dispatcher = Dispatcher()


async def stop_bot():
    await bot.send_message(chat_id=889732033, text='Бот остановлен!')


async def init_data():
    command.upgrade(config=Config(file_='./alembic.ini'), revision='head')

    uow = UnitOfWork()
    async with uow:
        admin = await uow.admin.find_one(Admin.user_id == config.bot.admin)
        if not admin:
            admin = Admin(user_id=config.bot.admin)
            await uow.admin.add_one(admin)
            await uow.commit()

    if not os.path.exists("db/data.json"):
        with open("db/data.json", 'w') as file:
            d = {'count': 0}
            json.dump(d, file, indent=4)


async def main() -> None:
    """
        Entry point
    """

    # dp.shutdown.register(stop_bot)
    scheduler = AsyncIOScheduler(timezone="Europe/Moscow")
    scheduler.add_job(send_scheduler_msg, 'cron', hour='*', minute='0')
    scheduler.add_job(PhotoService.get_all_photo, 'interval', days=1)
    scheduler.start()
    dp.message.middleware.register(DBMiddleware())
    dp.callback_query.middleware.register(DBMiddleware())
    dp.include_routers(user_handlers.router, admin_handlers.router)
    await set_commands(bot)
    await dp.start_polling(bot)


if __name__ == '__main__':
    while True:
        try:
            start_thread_flask()
            loop = asyncio.get_event_loop()

            asyncio.run(init_data())
            asyncio.run(PhotoService.get_all_photo())
            loop.create_task(main())
            loop.run_forever()
        except Exception as ex:
            logger.error(ex)

