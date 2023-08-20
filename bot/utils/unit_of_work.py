from abc import ABC, abstractmethod
from typing import Type

from db.base import async_session_maker
from db.repositories.admin_repository import AdminRepository
from db.repositories.links_repository import LinksRepository
from db.repositories.user_repository import UserRepository


class IUnitOfWork(ABC):
    users: UserRepository
    links: LinksRepository
    admin: AdminRepository

    @abstractmethod
    def __init__(self):
        ...

    @abstractmethod
    async def __aenter__(self):
        ...

    @abstractmethod
    async def __aexit__(self, *args):
        ...

    @abstractmethod
    async def commit(self):
        ...

    @abstractmethod
    async def rollback(self):
        ...


class UnitOfWork(IUnitOfWork):

    def __init__(self):
        self.session_factory = async_session_maker

    async def __aenter__(self):
        self.session = self.session_factory()

        self.users = UserRepository(self.session)
        self.links = LinksRepository(self.session)
        self.admin = AdminRepository(self.session)

    async def __aexit__(self, *args):
        await self.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
