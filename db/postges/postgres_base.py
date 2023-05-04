import asyncio

from sqlalchemy import create_engine, URL, Column, Integer, ForeignKey, VARCHAR, select
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession
from sqlalchemy.orm import DeclarativeBase, declarative_base
from typing import List

from sqlalchemy import Column, Integer, Boolean
from sqlalchemy.orm import relationship, mapped_column, Mapped

from bot.config_data.config import config

# class Base(DeclarativeBase): pass
Base = declarative_base()

url = config.postgres.get_url()


async def init_models():
    engine = create_async_engine_()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


def create_async_engine_():
    return create_async_engine(url, echo=True)


def create_async_session():
    engine = create_async_engine_()
    return async_sessionmaker(engine, expire_on_commit=False)


session = create_async_session()

# async def main():
#
#     session = create_async_session()
# async with session.
