import asyncio
from dataclasses import dataclass

from sqlalchemy import create_engine, URL, Column, Integer, ForeignKey, VARCHAR, select, String
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, declarative_base
from typing import List

from sqlalchemy import Column, Integer, Boolean
from sqlalchemy.orm import relationship, mapped_column, Mapped
from db.postges.test_db import BaseModel




# Base = declarative_base()

DATABASE = {
    'drivername': 'postgresql+asyncpg',  # Тут можно использовать MySQL или другой драйвер
    'host': 'localhost',
    'port': '8083',
    'username': 'admin',
    'password': 'admin',
    'database': 'db',
    'query': {}
}


# class ModelAdmin:
#     @classmethod
#     async def create(cls, **kwargs):
#         async_db_session.add(cls(**kwargs))
#         await async_db_session.commit()
#
#     @classmethod
#     async def update(cls, id, **kwargs):
#         query = (
#             sqlalchemy_update(cls)
#             .where(cls.id == id)
#             .values(**kwargs)
#             .execution_options(synchronize_session="fetch")
#         )
#
#         await async_db_session.execute(query)
#         await async_db_session.commit()
#
#     @classmethod
#     async def get(cls, id):
#         query = select(cls).where(cls.id == id)
#         results = await async_db_session.execute(query)
#         (result,) = results.one()
#         return result


class Parent(BaseModel):
    __tablename__ = "parent_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    children: Mapped[List["Child"]] = relationship(back_populates="parent")


class Child(BaseModel):
    __tablename__ = "child_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    parent_id: Mapped[int] = mapped_column(ForeignKey("parent_table.id"))
    parent: Mapped["Parent"] = relationship(back_populates="children")


class User(BaseModel):
    __tablename__ = "users"
    user_id: Mapped[int] = Column(Integer, primary_key=True)
    is_admin: Mapped[bool] = Column(Boolean, default=False)
    message_id_choise: Mapped[int | None] = mapped_column(default=None)
    dora_links: Mapped[List["Dora"]] = relationship("Dora", back_populates="admin")


class Admin(BaseModel):
    __tablename__ = "users"
    user_id: Mapped[int] = Column(Integer, primary_key=True)
    is_admin: Mapped[bool] = Column(Boolean, default=False)
    message_id_choise: Mapped[int | None] = mapped_column(default=None)
    dora_links: Mapped[List["Dora"]] = relationship("Dora", back_populates="admin")

class Dora(BaseModel):
    __tablename__ = "dora"
    link: Mapped[str] = mapped_column(String(32), primary_key=True)
    file_id: Mapped[str | None] = mapped_column(String(32), default=None)
    user_id: Mapped[int | None] = mapped_column(ForeignKey("users.user_id"))
    is_dataset: Mapped[bool] = mapped_column(Boolean, default=False)
    is_cool: Mapped[bool] = mapped_column(Boolean, default=False)
    admin: Mapped["User"] = relationship("User", back_populates="dora_links")


#
#
# class Child(Base):
#     __tablename__ = "child_table"
#     id = Column(Integer, primary_key=True)
#     name = Column(VARCHAR(32))
#     parent_id = Column(Integer, ForeignKey("parent_table.id"))
#     parent = relationship("Parent", back_populates="children")


async def init_models(engine, metadata):
    async with engine.begin() as conn:
        await conn.run_sync(metadata.drop_all)
        await conn.run_sync(metadata.create_all)


def create_async_engine_(url):
    return create_async_engine(url, echo=True)


def create_async_session(engine):
    return async_sessionmaker(engine, expire_on_commit=False)


async def main():
    engine = create_async_engine_(URL(**DATABASE))
    await init_models(engine, BaseModel.metadata)
    session = create_async_session(engine)

    dora1 = Dora(link="link1")
    dora2 = Dora(link="link2")
    user1 = User(user_id=35347853)
    user1.dora_links = []

    async with session() as session:
        session.add_all([dora1, dora2, user1])
        await session.commit()

        # dora3 = Dora(link="3")
        user1.dora_links.append(dora1)
        await session.commit()

        stmt = select(User)
        result = await session.execute(stmt)

        for user in result.scalars():
            user.is_admin = True
        await session.commit()
    # async with session() as conn:
    #     conn.add_all([user1, user2, book1, book2, review1, review2])
    #     await conn.commit()
    #     stmt = select(User)
    #     async_result = await conn.stream(stmt)
    #
    #     print(async_result)


asyncio.run(main())
