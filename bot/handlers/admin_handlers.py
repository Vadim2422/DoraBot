import datetime

from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.types import CallbackQuery, InputMediaPhoto
from sqlalchemy import select, func, desc, and_
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from db.models import Admin
from main import bot
from parsing.photo_service import PhotoService
from bot.config_data.config import config
from bot.keyboards.admin_keyboard import get_admin_ikb
from bot.utils.unit_of_work import IUnitOfWork
from db import Links

router = Router()
router.message.filter(lambda msg: msg.from_user.id == config.bot.admin)


@router.message(Command('help'))
async def help(message: types.Message):
    await message.answer(
        """/start - активация бота
/help - вывод возможных команд
/selection - отправить сообщение с добавлением фотографий
/start_sending - начало рассылки
/info - информация об оставшихся фото
/add_dataset - добавить датасет""")


@router.message(Command('selection'))
async def selection(message: types.Message, uow: IUnitOfWork):
    async with uow:
        admin: Admin = await uow.admin.find_one(Admin.user_id == message.from_user.id)
        if admin.file_id:
            selection_photo = await message.answer_photo(admin.file_id, reply_markup=get_admin_ikb())
            await bot.delete_message(message.chat.id, admin.selection_msg_id)
            new_file_id = selection_photo.photo[-1].file_id
            admin.selection_msg_id = selection_photo.message_id
            dora = await uow.links.find_one(Links.file_id == admin.file_id)
            admin.file_id = new_file_id
            dora.file_id = new_file_id
        else:
            dora: Links = await uow.links.find_random(file_id=None)
            if dora:
                new_message = await message.answer_photo(dora.link, reply_markup=get_admin_ikb())
                dora.file_id = new_message.photo[-1].file_id
                dora.unique_file_id = new_message.photo[-1].file_unique_id
                admin.selection_msg_id = new_message.message_id
                admin.file_id = dora.file_id
            else:
                await message.answer(f'Больше фотографий нет')
                return
        await uow.commit()


@router.message(Command('delete_last'))
async def delete_last(message: types.Message, session: async_sessionmaker):
    async with session() as session:
        stmt = select(Links).where(Links.date != None).order_by(desc(Links.date)).limit(1)
        dora: Links = await session.scalar(stmt)
        if dora:
            dora.date = None
            dora.is_cool = False
            dora.is_dataset = False
            await session.commit()
            await message.answer_photo(photo=dora.file_id, caption='Фото удалено')


@router.message(Command('start_sending'))
async def start_sending(message: types.Message):
    # start_sending_msg()
    await message.answer('Рассылка активирована')


@router.message(Command('info'))
async def info(message: types.Message, uow: IUnitOfWork):
    async with uow:
        count = await uow.links.count_records(is_dataset=True)
        await message.answer(f'В датасете {count} фото')


@router.message(Command('add_dataset'))
async def add_dataset(message: types.Message, uow: IUnitOfWork):
    msg = message.text.split()
    if len(msg) != 2:
        return
    link = msg[1]
    try:
        async with uow:
            await PhotoService.get_all_photo()
        await message.answer('Датасет добавлен')
    except Exception:
        await message.answer('Неудачно')


@router.callback_query(F.data.in_(['Cool', 'Trash']))
async def cool(query: CallbackQuery, uow: IUnitOfWork):
    async with uow:
        tmp = query.message.photo[-1].file_id
        new_dora: Links = await uow.links.find_random(file_id=None)
        if not new_dora:
            await query.message.delete()
            await query.message.answer(f'Больше фотографий нет')
        else:
            update_message = await query.message.edit_media(InputMediaPhoto(media=new_dora.link),
                                                            reply_markup=query.message.reply_markup)
            new_dora.file_id = update_message.photo[-1].file_id
            admin: Admin = await uow.admin.find_one(Admin.user_id == query.from_user.id)
            admin.file_id = new_dora.file_id
            await uow.commit()

        dora: Links = await uow.links.find_one(Links.file_id == tmp)
        if query.data == 'Cool':
            dora.is_cool = True
            dora.is_dataset = True
            dora.date = datetime.datetime.now()
            await query.answer('Фото добавлено в датасет')
            await PhotoService.add_photo_to_vk_album(dora.link)

        else:
            dora.is_cool = False
            dora.is_dataset = False
            await query.answer('В топку')
        dora.date = datetime.datetime.now()
        dora.admin_id = query.message.from_user.id
        await uow.commit()
