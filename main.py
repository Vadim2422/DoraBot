import asyncio
from aiogram import Bot, Dispatcher
from apscheduler.schedulers.asyncio import AsyncIOScheduler


from bot.middlewares.db_middleware import DBMiddleware
from bot.config_data.config import config
from bot.handlers import user_handlers, admin_handlers

from bot.utils.unit_of_work import UnitOfWork

from bot.utils.comands import set_commands
from db.models import Admin
from flask_service.service import start_thread_flask

bot: Bot = Bot(token=config.bot.token)
dp: Dispatcher = Dispatcher()
scheduler = AsyncIOScheduler(timezone="Europe/Moscow")


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

    dp.shutdown.register(stop_bot)
    dp.message.middleware.register(DBMiddleware())
    dp.callback_query.middleware.register(DBMiddleware())
    dp.include_routers(user_handlers.router, admin_handlers.router)
    await set_commands(bot)
    await dp.start_polling(bot)


if __name__ == '__main__':
    await init_data()
    start_thread_flask()
    asyncio.run(main())

