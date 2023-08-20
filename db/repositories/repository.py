from abc import ABC, abstractmethod

from sqlalchemy import select, delete, BinaryExpression, func
from sqlalchemy.ext.asyncio import AsyncSession


class AbstractRepository(ABC):

    @abstractmethod
    def __init__(self):
        raise NotImplementedError

    @abstractmethod
    async def add_one(self, model):
        raise NotImplementedError

    @abstractmethod
    def add_all(self, models):
        raise NotImplementedError

    @abstractmethod
    async def find_one(self, filters):
        raise NotImplementedError

    @abstractmethod
    async def find_all(self, where: BinaryExpression = None, filters: dict = None, orders: tuple = None):
        raise NotImplementedError

    @abstractmethod
    async def delete(self, **filters):
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository):
    model = None

    def __init__(self, session: AsyncSession):
        self.session = session

    async def count_records(self, **filters):
        stmt = select(func.count()).select_from(self.model).filter_by(**filters)
        return await self.session.scalar(stmt)

    async def find_random(self, **filters):
        stmt = select(self.model).filter_by(**filters).order_by(func.random()).limit(1)
        return await self.session.scalar(stmt)

    async def find_one(self, filters):
        stmt = select(self.model).filter(filters)
        return await self.session.scalar(stmt)

    async def add_one(self, model_db):
        self.session.add(model_db)

    async def delete(self, **filters):
        stmt = delete(self.model).filter_by(**filters)
        await self.session.execute(stmt)

    async def find_all(self, where: BinaryExpression = None, filters: dict = None, orders: tuple = None):
        stmt = select(self.model)
        if where is not None:
            stmt = stmt.where(where)
        if filters:
            stmt = stmt.filter_by(**filters)
        if orders:
            stmt = stmt.order_by(*orders)
        res = [row for row in (await self.session.scalars(stmt)).unique()]
        return res

    def add_all(self, models):
        self.session.add_all(models)
