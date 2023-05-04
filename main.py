import pathlib
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from bot.middlewares.db_middleware import DBMiddleware
from bot.config_data.config import config
from bot.handlers import admin_handlers, user_handlers


from bot.config_data.photo import Photo
from bot.config_data.start_sending import start_sending_msg
from bot.files.json_files import create_files
from bot.send_photo import send_user, send_admin

from bot.handlers.error_handlers import register_error_handler
from db.postges.postgres_base import init_models

from db import User, Dora
from bot.utils.comands import set_commands

from parsing.parsing import get_all_photo

bot: Bot = Bot(token=config.bot.token)
dp: Dispatcher = Dispatcher()


async def stop_bot():
    await bot.send_message(chat_id=889732033, text='Бот остановлен!')


async def main() -> None:
    """
        Entry point
    """
    # await init_models()

    # dp.shutdown.register(stop_bot)
    dp.message.middleware.register(DBMiddleware())
    dp.callback_query.middleware.register(DBMiddleware())
    dp.include_routers(admin_handlers.router, user_handlers.router)
    await dp.start_polling(bot)
    #
    # # await set_commands(bot)
    # register_handler(dp)
    #
    # create_files()
    # # try:
    # photo: Photo = Photo()
    # if not photo.count_current_photo:
    #     await send_admin(bot, photo)
    # # list_cor = [asyncio.create_task(dp.start_polling()), asyncio.create_task(send_user(bot, photo))]
    # list_cor = [asyncio.create_task(dp.start_polling()), asyncio.create_task(start_sending(bot, photo))]
    # await asyncio.gather(*list_cor)

    # except Exception as _ex:
    #     print(_ex)


if __name__ == '__main__':
    asyncio.run(main())
    # link = 'https://vk.com/cutedori'
    # if not pathlib.Path('src/links.json').is_file():
    #     asyncio.run(get_all_photo(link))
    # asyncio.run(main())
