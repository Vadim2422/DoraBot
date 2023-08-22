import io
import json

from aiogram import types, Dispatcher, F
from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import CallbackQuery, InputMedia, InputFile, InputMediaPhoto
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from bot.config_data.photo import Photo
from bot.utils.unit_of_work import IUnitOfWork
from db import User

router = Router()


@router.message(CommandStart())
async def cmd_start(msg: types.Message, uow: IUnitOfWork) -> None:
    async with uow:
        user = await uow.users.find_one(User.user_id == msg.from_user.id)
        if user:
            if user.is_dora:
                await msg.answer('Вы уже подписаны')
                return
            else:
                user.is_dora = True
                await uow.commit()
        else:
            await uow.users.add_one(User(user_id=msg.from_user.id))
            await uow.commit()
        await msg.answer('Вы успешно подписались на рассылку Доры каждый час')


# @router.message(Command('help'))
# async def help(message: types.Message):
#     await message.answer("user_help")


@router.message(Command('stop'))
async def stop(message: types.Message, uow: IUnitOfWork):
    async with uow:
        user = await uow.users.find_one(User.user_id == message.from_user.id)
        user.is_dora = False
        await uow.commit()
        await message.answer('Вы отписались от рассылки')



# @router.message(Command('dora'))
# async def dora(message: types.Message, session):
#     async with session() as session:
#         stmt = select(User).where(User.user_id == message.from_user.id)
#         user = await session.scalar(stmt)
#         user.is_dora = True
#         await session.commit()
#         await message.answer('Вы успешно подписались на рассылку Доры')
