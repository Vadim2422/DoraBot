from aiogram import Dispatcher

from bot.errors.photos_are_over import PhotosAreOverError


async def photos_are_over(update, exception):
    print(update)
    return True


def register_error_handler(dp: Dispatcher) -> None:
    dp.register_errors_handler(photos_are_over, exception=PhotosAreOverError)

