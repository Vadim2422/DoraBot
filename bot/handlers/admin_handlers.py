import io
import re

from aiogram import Router, types, F, Bot
from aiogram.client.session import aiohttp
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import InputFile, CallbackQuery, InputMediaPhoto
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from bot.keyboards.admin_keyboard import get_admin_ikb
from bot.middlewares.admin_middleware import AdminMiddleware
from bot.config_data.config import config
from bot.keyboards.user_keyboards import get_set_admin_kb
from bot.states.admin_state import AddAdmin
from db import User, Dora
from parsing.parsing import get_all_photo
from bot.config_data.start_sending import start_sending_msg

router = Router()
# router.message.middleware.register(AdminMiddleware())
router.message.filter(lambda msg: msg.from_user.id == config.bot.admin)


@router.message(Command('help'))
async def help(message: types.Message):
    await message.answer("""/start - активация бота
    /help - вывод возможных команд
    /selection - отправить сообщение с добавлением фотографий
    /start_sending - начало рассылки
    /info - информация об оставшихся фото
    /add_dataset - добавить датасет
    """)

@router.message(Command('selection'))
async def selection(message: types.Message, session):
    async with session() as session:
        stmt = select(Dora) \
            .where(Dora.file_id == None) \
            .order_by(func.random()) \
            .limit(1)
        dora = await session.scalar(stmt)
        if not dora:
            await message.answer(f'Больше фотографий нет')
        else:
            new_message = await message.answer_photo(dora.link, reply_markup=get_admin_ikb())
            dora.file_id = new_message.photo[-1].file_id
            await session.commit()


@router.message(Command('start_sending'))
async def start_sending(message: types.Message):
    start_sending_msg()
    await message.answer('Рассылка активирована')


@router.message(Command('info'))
async def info(message: types.Message, session):
    async with session() as session:
        session: AsyncSession
        stmt = select(func.count()).where(Dora.is_dataset == True).select_from(Dora)
        count = await session.scalar(stmt)
        await message.answer(f'В датасете {count}')


@router.message(Command('add_dataset'))
async def add_dataset(message: types.Message):
    msg = message.text.split()
    if len(msg) != 2:
        return
    link = msg[1]
    try:
        await get_all_photo(link)
        await message.answer('Датасет добавлен')
    except Exception:
        await message.answer('Неудачно')


@router.callback_query(F.data.in_(['Cool', 'Trash']))
async def cool(query: CallbackQuery, session):
    async with session() as session:
        stmt = select(Dora).where(Dora.file_id == query.message.photo[-1].file_id)
        dora = await session.scalar(stmt)
        if query.data == 'Cool':
            dora.is_cool = True
            dora.is_dataset = True
            await query.answer('Фото добавлено в датасет')
        else:
            dora.is_cool = False
            dora.is_dataset = False
            await query.answer('Фото отправляется в мусор')
        await session.commit()
        stmt = select(Dora).where(Dora.file_id == None).order_by(func.random()).limit(1)
        new_dora: Dora = await session.scalar(stmt)
        if not new_dora:
            await query.message.delete()
            await query.message.answer(f'Больше фотографий нет')
        else:
            update_message = await query.message.edit_media(InputMediaPhoto(media=new_dora.link),
                                                            reply_markup=query.message.reply_markup)
            new_dora.file_id = update_message.photo[-1].file_id
            await session.commit()

# @router.callback_query(F.data == 'Trash')
# async def trash(query: CallbackQuery, session):
#     async with session() as session:
#         stmt = select(Dora).where(Dora.file_id == query.message.photo[-1].file_id)
#         dora = await session.scalar(stmt)
#         dora.is_cool = False
#         dora.is_dataset = False
#         await session.commit()
#         stmt = select(Dora).where(Dora.file_id == None).order_by(func.random()).limit(1)
#         new_dora: Dora = await session.scalar(stmt)
#         if not new_dora:
#             await query.message.delete()
#             await query.message.answer(f'Больше фотографий нет')
#         else:
#             update_message = await query.message.edit_media(InputMediaPhoto(media=new_dora.link),
#                                                             reply_markup=query.message.reply_markup)
#             new_dora.file_id = update_message.photo[-1].file_id
#             await session.commit()
#             await query.answer('Фото добавлено в датасет')

# @router.message(Command('set_admin'))
# async def set_admin(message: types.Message, state: FSMContext):
#     await state.set_state(AddAdmin.contact)
#     await message.answer('get admin')
#
#
# @router.message(AddAdmin.contact, F.contact)
# async def admin(message: types.Message, state: FSMContext, session):
#     await state.clear()
#     async with session() as session:
#         session: AsyncSession
#         stmt = select(User).where(User.user_id == message.contact.user_id and )
#         user: User = await session.scalar(stmt)
#         if user:
#             user.admin = True
#             stmt = select(Dora).where(Dora.admin == None).order_by(func.random).limit(2)
#             dora_link = await session.query(User)
#             dora_link
#             send_msg = await bot.send_message(user.user_id, )
#
#     await message.answer(message.contact.user_id.__str__())
