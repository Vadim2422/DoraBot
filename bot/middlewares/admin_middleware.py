from typing import Callable, Dict, Any, Awaitable
from aiogram.types import Message
from aiogram import BaseMiddleware

from bot.config_data.config import config
from db.postges.postgres_base import session


class AdminMiddleware(BaseMiddleware):

    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ) -> Any:
        if event.from_user.id == config.bot.admin:
            return await handler(event, data)

