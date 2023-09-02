import asyncio
import json
import os.path
import time
from threading import Thread

import uvicorn
from aiogram.types import Update
from alembic import command
from alembic.config import Config
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram import Bot, Dispatcher
from fastapi import FastAPI, Request

from bot.config_data.schedule_sending import send_scheduler_msg
from bot.middlewares.db_middleware import DBMiddleware
from bot.config_data.config import config
from bot.handlers import user_handlers, admin_handlers

from bot.utils.unit_of_work import UnitOfWork

from bot.utils.comands import set_commands
from db.models import Admin
from logs.logger import logger
from parsing.photo_service import PhotoService

WEBHOOK_PATH = f"/bot/{config.secret}"
WEBHOOK_URL = "https://9743-31-131-210-133.ngrok.io" + WEBHOOK_PATH

bot: Bot = Bot(token=config.bot.token)
dp: Dispatcher = Dispatcher()

app = FastAPI()


@app.get("/")
async def index():
    return "Ok"


@app.head("/")
async def head():
    return "Head"


@app.on_event("startup")
async def start():
    await bot.set_webhook(WEBHOOK_URL)


@app.post(WEBHOOK_PATH)
async def webhook(request: Request):
    update = Update(**await request.json())
    await dp.feed_update(bot, update)


@app.on_event("shutdown")
async def shutdown():
    await bot.session.close()


async def start_scheduler():
    scheduler = AsyncIOScheduler(timezone="Europe/Moscow")
    scheduler.add_job(send_scheduler_msg, 'cron', hour='*', minute='0')
    scheduler.add_job(PhotoService.get_all_photo, 'interval', days=1)
    scheduler.start()
    while True:
        await asyncio.sleep(5)


def start_scheduler_thread():
    t = Thread(target=start_scheduler)
    t.start()


def start_uvicorn():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    uvicorn.run(app, host='0.0.0.0', port=8080)


def start_api_thread():
    t = Thread(target=start_uvicorn)
    t.start()


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
    await set_commands(bot)
    dp.message.middleware.register(DBMiddleware())
    dp.callback_query.middleware.register(DBMiddleware())
    dp.include_routers(user_handlers.router, admin_handlers.router)
    task = asyncio.create_task(start_scheduler())
    await asyncio.gather(task)
    # scheduler = AsyncIOScheduler(timezone="Europe/Moscow")
    # scheduler.add_job(send_scheduler_msg, 'cron', hour='*', minute='0')
    # scheduler.add_job(PhotoService.get_all_photo, 'interval', days=1)
    # scheduler.start()
    # while True:
    #     await asyncio.sleep(10)
    # config_uvicorn = uvicorn.Config(app=app, host="0.0.0.0", port=8080)
    # server = uvicorn.Server(config_uvicorn)
    # task = asyncio.create_task(server.serve())
    # await asyncio.gather(task)

    # await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
    start_api_thread()
    asyncio.run(init_data())
# uvicorn.run(app, host='0.0.0.0', port=8080)
# start_api_thread()
# start_scheduler_thread()
# while True:
#     time.sleep(5)
# asyncio.run(init_data())
# while True:

# uvicorn.run(app, host='0.0.0.0', port=8080)

# try:
#     asyncio.run(main())
# except Exception as ex:
#     logger.error(ex)
