from typing import Callable, Dict, Any, Awaitable, Annotated
from aiogram.types import Message
from aiogram import BaseMiddleware

from bot.utils.unit_of_work import UnitOfWork, IUnitOfWork


class DBMiddleware(BaseMiddleware):

    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ) -> Any:
        data['uow'] = UnitOfWork()
        return await handler(event, data)
