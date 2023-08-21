import asyncio
from threading import Thread

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

bot: Bot = Bot(token=config.bot.token)
dp: Dispatcher = Dispatcher()


async def stop_bot():
    await bot.send_message(chat_id=889732033, text='Бот остановлен!')


async def init_data():
    uow = UnitOfWork()
    async with uow:
        admin = await uow.admin.find_one(Admin.user_id == config.bot.admin)
        if not admin:
            admin = Admin(user_id=config.bot.admin)
            await uow.admin.add_one(admin)
            await uow.commit()


async def main() -> None:
    """
        Entry point
    """

    # dp.shutdown.register(stop_bot)
    scheduler = AsyncIOScheduler(timezone="Europe/Moscow")
    scheduler.add_job(send_scheduler_msg, 'cron', hour='*', minute='0')
    scheduler.start()
    dp.message.middleware.register(DBMiddleware())
    dp.callback_query.middleware.register(DBMiddleware())
    dp.include_routers(user_handlers.router, admin_handlers.router)
    await set_commands(bot)
    await dp.start_polling(bot)


if __name__ == '__main__':
    start_thread_flask()

    loop = asyncio.get_event_loop()
    asyncio.run(init_data())
    loop.create_task(main())
    loop.run_forever()
