from typing import Callable, Dict, Any, Awaitable

from aiogram.dispatcher.flags import get_flag
from aiogram.types import Message
from aiogram import BaseMiddleware

from main import scheduler


class SchedulerMiddleware(BaseMiddleware):

    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ) -> Any:
        is_scheduler = get_flag(data, 'scheduler')
        if is_scheduler:
            data['scheduler'] = scheduler
        return await handler(event, data)
