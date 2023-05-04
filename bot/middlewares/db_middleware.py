from typing import Callable, Dict, Any, Awaitable
from aiogram.types import Message
from aiogram import BaseMiddleware
from db.postges.postgres_base import session


class DBMiddleware(BaseMiddleware):

    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ) -> Any:
        data['session'] = session
        return await handler(event, data)
