import io
import json

from aiogram import types, Dispatcher, F
from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import CallbackQuery, InputMedia, InputFile, InputMediaPhoto
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from bot.config_data.photo import Photo
from db import User

router = Router()


@router.message(CommandStart())
async def cmd_start(msg: types.Message, session) -> None:
    async with session() as session:
        session: AsyncSession
        stmt = select(User).where(User.user_id == msg.from_user.id)
        user = await session.scalar(stmt)
        if user:
            if user.is_dora:
                await msg.answer('Вы уже подписаны')
                return
        session.add(User(user_id=msg.from_user.id))
        await session.commit()
        await msg.answer('Вы успешно подписались на рассылку Доры каждый час')


@router.message(Command('help'))
async def help(message: types.Message):
    await message.answer("""/start - подписка на рассылку
    /help - вывод возможных команд
    /stop - остановка рассылки
    /info - информация об оставшихся фото
    /add_dataset - добавить датасет
    """)


@router.message(Command('stop'))
async def stop(message: types.Message, session):
    async with session() as session:
        stmt = select(User).where(User.user_id == message.from_user.id)
        user = session.scalar(stmt)
        user.is_dora = False
        await session.commit()
        await message.answer('Вы отписались от рассылки')

# @router.message(Command('dora'))
# async def dora(message: types.Message, session):
#     async with session() as session:
#         stmt = select(User).where(User.user_id == message.from_user.id)
#         user = await session.scalar(stmt)
#         user.is_dora = True
#         await session.commit()
#         await message.answer('Вы успешно подписались на рассылку Доры')
